from django.conf import settings
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .models import ConnectedService
from django.core import signing
from django.contrib.auth.models import User
import secrets
from django.utils import timezone
import requests
from .utils import validate_token
from urllib.parse import urlencode
import hashlib
import base64
from datetime import timedelta
from .serializers import ConnectedServiceSerializer


# Views
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_connected_services(request):

    connected_services = ConnectedService.objects.filter(user=request.user)
    serializer = ConnectedServiceSerializer(connected_services, many=True)

    return Response({"services": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def google_connect(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
        ],
        redirect_uri="http://localhost:8000/api/services/google/callback/",
    )

    code_verifier = secrets.token_urlsafe(64)
    flow.code_verifier = code_verifier

    signed_state = signing.dumps(
        {
            "user_id": request.user.id,
            "code_verifier": flow.code_verifier,
        }
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        state=signed_state,
    )

    return Response({"auth_url": auth_url})


@api_view(["GET"])
def google_callback(request):

    code = request.GET.get("code")
    state = request.GET.get("state")

    try:
        data = signing.loads(state, max_age=300)

    except signing.BadSignature:
        return Response(
            {"error": "Invalid or tampered state"},
            status=400,
        )

    user_id = data["user_id"]
    code_verifier = data["code_verifier"]

    user = User.objects.get(id=user_id)

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
        ],
        redirect_uri="http://localhost:8000/api/services/google/callback/",
    )
    flow.code_verifier = code_verifier
    flow.fetch_token(code=code)

    credentials = flow.credentials
    access_token = credentials.token
    refresh_token = credentials.refresh_token

    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        google_requests.Request(),
        settings.GOOGLE_CLIENT_ID,
    )

    account_id = id_info["email"]
    print(credentials.expiry.tzinfo)
    ConnectedService.objects.update_or_create(
        user=user,
        name="google",
        account_id=account_id,
        defaults={
            "access_token": access_token,
            "access_expiry": timezone.make_aware(credentials.expiry),
            "refresh_token": refresh_token,
        },
    )

    return Response(
        {"message": "Google account connected successfully", "email": account_id}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def google_files(request):

    user = request.user
    account_id = request.GET.get("account_id")
    path = request.GET.get("path", "root")

    try:
        cs = ConnectedService.objects.get(
            user=user, name="google", account_id=account_id
        )
    except ConnectedService.DoesNotExist:
        return Response({"error": "Service Not Found!"}, status=404)

    access_token = validate_token(cs)

    response = requests.get(
        "https://www.googleapis.com/drive/v3/files",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"fields": "files(id,name,mimeType)", "q": f"'{path}' in parents"},
    )

    return Response(response.json()["files"])


# DROPBOX CONNECTION
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dropbox_connect(request):

    redirect_uri = "http://localhost:8000/api/services/dropbox/callback/"

    code_verifier = secrets.token_urlsafe(64)
    signed_state = signing.dumps(
        {
            "user_id": request.user.id,
            "code_verifier": code_verifier,
        }
    )

    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )

    params = {
        "client_id": settings.DROPBOX_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "token_access_type": "offline",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": signed_state,
    }

    auth_url = f"https://www.dropbox.com/oauth2/authorize?{urlencode(params)}"
    return Response({"auth_url": auth_url})


@api_view(["GET"])
@permission_classes([AllowAny])
def dropbox_callback(request):

    code = request.GET.get("code")
    state = request.GET.get("state")

    try:
        data = signing.loads(state, max_age=300)
    except signing.BadSignature:
        return Response({"error": "Invalid or tampered state"}, status=400)

    code_verifier = data["code_verifier"]
    user_id = data["user_id"]

    url = "https://api.dropboxapi.com/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier,
        "client_id": settings.DROPBOX_CLIENT_ID,
        "client_secret": settings.DROPBOX_CLIENT_SECRET,
        "redirect_uri": "http://localhost:8000/api/services/dropbox/callback/",
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        return Response({"error": "Server Error"}, status=400)

    data = response.json()

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User Not Found"}, status=404)

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]
    account_id = data["account_id"]
    access_expiry = timezone.now() + timedelta(seconds=data["expires_in"])

    ConnectedService.objects.update_or_create(
        user=user,
        name="dropbox",
        account_id=account_id,
        defaults={
            "access_token": access_token,
            "access_expiry": access_expiry,
            "refresh_token": refresh_token,
        },
    )

    return Response(
        {"message": "Dropbox account connected successfully", "account_id": account_id}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dropbox_files(request):

    user = request.user
    account_id = request.GET.get("account_id")
    path = request.GET.get("path", "")

    # Translating root value for path as "" cause thats what dropbox consider as root
    if path == "root":
        path = ""

    try:
        cs = ConnectedService.objects.get(
            user=user, account_id=account_id, name="dropbox"
        )
    except ConnectedService.DoesNotExist:
        return Response({"error": "Service Not Found"}, status=404)

    access_token = validate_token(cs)

    url = "https://api.dropboxapi.com/2/files/list_folder"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {"path": path}

    response = requests.post(url, headers=headers, json=data)
    entries = response.json()["entries"]

    return Response(entries)

from django.conf import settings
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .models import ConnectedService
from django.core import signing
from django.contrib.auth.models import User
import secrets


# Views
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

    account_email = id_info["email"]

    ConnectedService.objects.create(
        name="google",
        account_email=account_email,
        access_token=access_token,
        refresh_token=refresh_token,
        user=user,
    )

    return Response(
        {"message": "Google account connected successfully", "email": account_email}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def google_files(request):
    user = request.user
    connection = ConnectedService.objects.get(user=user, name="google")
    access_token = connection.access_token

    import requests

    response = requests.get(
        "https://www.googleapis.com/drive/v3/files",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"fields": "files(id,name,mimeType)"},
    )

    return Response(response.json())

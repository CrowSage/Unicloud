from django.conf import settings
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .models import ConnectedService


# Views
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

    auth_url, state = flow.authorization_url(access_type="offline", prompt="consent")

    request.session["oauth_state"] = state

    return redirect(auth_url)


@api_view(["GET"])
def google_callback(request):

    code = request.GET.get("code")
    state = request.GET.get("state")

    saved_state = request.session.pop("oauth_state", None)

    if not saved_state or saved_state != state:
        return Response(
            {"error": "Secure session mismatch. Please try again."},
            status=400,
        )

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
        user=request.user,
    )

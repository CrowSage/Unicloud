from django.conf import settings
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect


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
        scopes=["https://www.googleapis.com/auth/drive"],
        redirect_uri="http://localhost:8000/api/services/google/callback/",
    )

    auth_url, state = flow.authorization_url(access_type="offline", prompt="consent")
    return redirect(auth_url)

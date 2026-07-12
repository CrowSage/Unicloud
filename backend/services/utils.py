from django.utils import timezone
from datetime import timedelta
import requests
from django.conf import settings


def validate_token(connected_service):

    if connected_service.access_expiry < timezone.now() + timedelta(seconds=60):

        service_name = connected_service.name.upper()

        if service_name == "GOOGLE":
            url = "https://oauth2.googleapis.com/token"
        elif service_name == "DROPBOX":
            url = "https://api.dropboxapi.com/oauth2/token"

        payload = {
            "client_id": getattr(settings, f"{service_name}_CLIENT_ID"),
            "client_secret": getattr(settings, f"{service_name}_CLIENT_SECRET"),
            "refresh_token": connected_service.refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(url=url, data=payload)

        if response.status_code != 200:
            raise Exception(f"{service_name} refresh token invalid, reconnect required")

        data = response.json()

        access_token = data.get("access_token")

        connected_service.access_token = access_token
        connected_service.access_expiry = timezone.now() + timedelta(
            seconds=data.get("expires_in")
        )

        connected_service.save()

    return connected_service.access_token

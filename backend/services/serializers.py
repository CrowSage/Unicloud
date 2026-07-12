from rest_framework.serializers import ModelSerializer
from .models import ConnectedService


class ConnectedServiceSerializer(ModelSerializer):

    class Meta:
        model = ConnectedService
        fields = ["account_id", "name"]

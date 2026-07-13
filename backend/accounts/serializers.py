from django.contrib.auth.models import User
from rest_framework import serializers
import re


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    # Username Validation
    def validate_username(self, value):

        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be greater then 3 characters!"
            )

        elif not re.fullmatch(r"^(?=.*[A-Za-z])[A-Za-z0-9_-]{3,30}$", value):
            raise serializers.ValidationError("Username is not allowed!")

        return value

    # Password Validation
    def validate_password(self, value):

        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be greater then 8 characters"
            )

        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

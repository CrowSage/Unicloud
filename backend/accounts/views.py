from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User Created Successfully!"}, status=201)

    return Response({"error": serializer.errors}, status=400)

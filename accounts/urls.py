from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    path("register/", view=views.register),
    path("login/", TokenObtainPairView.as_view()),
]

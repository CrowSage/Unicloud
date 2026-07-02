from django.urls import path
from . import views

urlpatterns = [
    path("google/connect/", views.google_connect),
]

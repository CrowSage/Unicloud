from django.urls import path
from . import views

urlpatterns = [
    path("google/connect/", views.google_connect),
    path("google/callback/", views.google_callback),
    path("google/files/", views.google_files),
]

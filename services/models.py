from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ConnectedService(models.Model):
    NAME_CHOICES = [
        ("google", "Google"),
        ("dropbox", "DropBox"),
    ]

    name = models.CharField(choices=NAME_CHOICES, default="google")
    account_email = models.CharField(max_length=255)
    access_token = models.TextField()
    refresh_token = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class meta:
        unique_together = ("user", "name", "account_email")

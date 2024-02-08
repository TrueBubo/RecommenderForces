from django.contrib.auth.models import User
from django.db import models


def defaultDict():
    return {}

# Extension of default user moder
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    preferences = models.JSONField(default=defaultDict) # tag: user rating mapping

    def __str__(self):
        return str(self.user)


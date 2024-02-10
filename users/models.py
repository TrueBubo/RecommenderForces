from django.contrib.auth.models import User
from django.db import models


def defaultDict():
    return {"rating": 800}

def defaultList():
    return []

# Extension of default user moder
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    preferences = models.JSONField(default=defaultDict) # rating: average rating + tag: [user rating mapping, number of rated with given tag]
    rated_problems = models.JSONField(default=defaultList) # id of problems

    def __str__(self):
        return str(self.user)


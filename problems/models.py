from django.db import models

# Create your models here.

class Problem(models.Model):
    problem_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=30)
    rating = models.IntegerField()
    tags = models.JSONField()

    def __str__(self):
        return f"{self.problem_id} {self.name}"



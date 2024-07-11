from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDescription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1024, blank=True)


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    solved_tests = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    time = models.TimeField(blank=True)
    title = models.CharField(max_length=60, blank=True)
    description = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)


class Question(models.Model):
    question = models.CharField(max_length=255, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    multiple_ans = models.BooleanField(default=False)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=255, blank=True)
    right_answer = models.BooleanField(default=False)


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mark = models.IntegerField(blank=True)
    start_at = models.DateTimeField(blank=True, auto_now_add=True)
    finish_at = models.DateTimeField(blank=True, auto_now_add=True)
    time = models.TimeField(blank=True, auto_now_add=True)


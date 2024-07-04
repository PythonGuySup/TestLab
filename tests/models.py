from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)


class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    time = models.TimeField(null=True)
    title = models.CharField(max_length=60, null=True)
    description = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


class Question(models.Model):
    question = models.CharField(max_length=255, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    multiple_ans = models.BooleanField(default=False)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=255, null=True)
    right_answer = models.BooleanField(default=False)


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mark = models.FloatField(null=True)
    start_at = models.DateTimeField(null=True)
    finish_at = models.DateTimeField(null=True)
    time = models.TimeField(null=True)

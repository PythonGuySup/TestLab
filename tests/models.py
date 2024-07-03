from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)


class Test(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time = models.TimeField()
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Question(models.Model):
    question = models.CharField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    multiple_ans = models.BooleanField(default=False)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    right_answer = models.BooleanField(default=False)


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.FloatField()
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()
    time = models.TimeField()

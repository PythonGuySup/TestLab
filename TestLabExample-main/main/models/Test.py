from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=40, blank=True)
    info = models.CharField(max_length=300, blank=True)

from django.contrib import admin
from .models import UserDescription, UserScore

# Register your models here.

admin.site.register(UserDescription)
admin.site.register(UserScore)
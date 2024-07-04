from django.urls import path
from users.views import register, profile

urlpatterns = [
    path('register/', register, name='register'),
    path('profile', profile, name='profile')
]
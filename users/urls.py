from django.urls import path
from users.views import register, profile, login_view, logout_view, stats, my_tests

urlpatterns = [
    path('register/', register, name='register'),
    path('profile', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('statics/', stats, name='stats'),
    path('my_tests/', my_tests, name="my_tests")
]
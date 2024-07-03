from django.urls import path
# from main import views

from tests import views

urlpatterns = [
    path('constructor/', views.constructor, name='constructor')
]
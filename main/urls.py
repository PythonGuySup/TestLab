from django.urls import path
from main import views

urlpatterns = [
    path('<str:pg>', views.home_page, name='home_page'),
]

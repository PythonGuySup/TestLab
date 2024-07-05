from django.urls import path
from main import views

urlpatterns = [
    path('<int:page>', views.home_page, name='home_page'),
]

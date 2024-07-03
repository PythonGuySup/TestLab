from django.urls import path
from . import views

urlpatterns = [
    path("<int:test_id>/", views.test_detail, name="test_detail"),
    path('<int:test_id>/execution/', views.test_questions, name='test_questions'),
]
from django.urls import path
from tests import views

urlpatterns = [
    path("<int:test_id>/", views.test_detail, name="test_detail"),
    path('<int:test_id>/execution/', views.test_questions, name='test_questions'),
    path('constructor/', views.constructor, name='constructor'),
    path('constructor/<int:test_id>', views.constructor, name='reconstructor'),
    path('constructor_result/', views.contructor_result, name='constructor_result'),
    path('constructor_result/<int:test_id>', views.contructor_result, name='reconstructor_result'),
]
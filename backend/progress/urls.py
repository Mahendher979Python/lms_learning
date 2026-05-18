from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_progress, name='admin_progress'),
    path('trainer/', views.trainer_progress, name='trainer_progress'),
    path('', views.student_progress, name='student_progress'),
]

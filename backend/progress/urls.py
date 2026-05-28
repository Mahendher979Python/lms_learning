from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_progress, name='admin_progress'),
    path('trainer/', views.trainer_progress, name='trainer_progress'),
    # Compatibility route (in case someone tries to open the template name as a URL)
    path('trainer_progress.html', views.trainer_progress, name='trainer_progress_html'),
    path('', views.student_progress, name='student_progress'),
]

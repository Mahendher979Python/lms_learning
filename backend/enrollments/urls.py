from django.urls import path
from . import views

urlpatterns = [
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('admin/', views.admin_enrollments, name='admin_enrollments'),
    path('approve/<int:id>/', views.approve_enrollment, name='approve_enrollment'),
]

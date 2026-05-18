from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_attendance, name='student_attendance'),
    path('login/', views.login_time, name='login_time'),
    path('logout/', views.logout_time, name='logout_time'),
    path('logout-attendance/', views.logout_attendance, name='logout_attendance'),
    path('start-break/', views.start_break, name='start_break'),
    path('end-break/', views.end_break, name='end_break'),
    path('face-attendance/', views.face_attendance, name='face_attendance'),
    path('auto-location/', views.auto_location, name='auto_location'),
    path('track-location/', views.track_location, name='track_location'),
    path('student/', views.student_attendance, name='student_attendance'),
    path('trainer/', views.trainer_attendance, name='trainer_attendance'),
    path('trainer/students/', views.assigned_students, name='assigned_students'),
    path('trainer/student/<int:user_id>/', views.student_attendance_view, name='student_attendance_view'),
    path('student/<int:user_id>/', views.student_detail_attendance, name='student_detail'),
    path('admin/', views.admin_attendance, name='admin_attendance'),
    path('latest-location/', views.latest_location, name='latest_location'),
    path('attendance-data/', views.attendance_data, name='attendance_data'),
    path('prediction/', views.attendance_prediction, name='attendance_prediction'),
    path('attendance/export/', views.export_attendance_csv, name='export_attendance_csv'),
    # ✅ NEW — admin fetch any user's latest location for the modal map
    path('user-location/<int:user_id>/', views.user_location, name='user_location'),
]
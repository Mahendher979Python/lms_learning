from django.urls import path
from . import views



urlpatterns = [
    # Admin
    path('admin-courses/', views.admin_courses, name='admin_courses'),
    path('admin-payments/', views.admin_payments, name='admin_payments'),
    path('mark-payment-success/<int:payment_id>/', views.mark_payment_success, name='mark_payment_success'),
    path('admin-create-course/', views.admin_create_course, name='admin_create_course'),
    path('admin-create-topic/', views.admin_create_topic, name='admin_create_topic'),
    path('edit-course/<int:id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:id>/', views.delete_course, name='delete_course'),

    # Trainer
    path('trainer-courses/', views.trainer_courses, name='trainer_courses'),
    path('trainer-create-topic/', views.trainer_create_topic, name='trainer_create_topic'),
    path('edit-topic/<int:id>/', views.edit_topic, name='edit_topic'),
    path('delete-topic/<int:id>/', views.delete_topic, name='delete_topic'),

    # Student
    path('student-courses/', views.student_courses, name='student_courses'),

    # Course Detail
    path('course-detail/<int:id>/', views.course_detail, name='course_detail'),

    # Payment
    path('create-payment/<int:course_id>/', views.create_payment, name='create_payment'),
    path('payment-success/<int:course_id>/', views.payment_success, name='payment_success'),
    path("webhook/", views.razorpay_webhook),

     # =========================
    # CERTIFICATES
    # =========================
    # path('student/certificates/',views.student_certificates,name='student_certificates'),
    # path('certificate/view/<int:id>/',views.view_certificate,name='view_certificate'),
    # path('certificate/download/<int:id>/',views.download_certificate,name='download_certificate'),
    path('assigned-courses/', views.assigned_courses, name='assigned_courses'),
    path('topic/<int:id>/', views.view_topic, name='view_topic'),
    path(
    'assigned-course/<int:id>/',
    views.assigned_course_detail,
    name='assigned_course_detail'
),

]

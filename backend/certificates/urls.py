from django.urls import path
from . import views

urlpatterns = [

    path(
        'send/<int:course_id>/<int:student_id>/',
        views.send_certificate_request,
        name='send_certificate_request'
    ),

    path(
        'admin/requests/',
        views.admin_certificate_requests,
        name='admin_certificate_requests'
    ),

    path(
        'approve/<int:certificate_id>/',
        views.approve_certificate,
        name='approve_certificate'
    ),

    path(
        'reject/<int:certificate_id>/',
        views.reject_certificate,
        name='reject_certificate'
    ),

    path(
        'view/<int:certificate_id>/',
        views.view_certificate,
        name='view_certificate'
    ),

    path(
        'download/<int:certificate_id>/',
        views.download_certificate,
        name='download_certificate'
    ),

    path(
        'email/<int:certificate_id>/',
        views.email_certificate,
        name='email_certificate'
    ),

    path(
        'my-certificates/',
        views.my_certificates,
        name='my_certificates'
    ),

]
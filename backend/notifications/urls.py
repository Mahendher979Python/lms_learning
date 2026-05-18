from django.urls import path
from . import views

urlpatterns = [

    # STUDENT
    path(
        'student/',
        views.student_notifications,
        name='student_notifications'
    ),

    # TRAINER
    path(
        'trainer/',
        views.trainer_notifications,
        name='trainer_notifications'
    ),

    # ADMIN
    path(
        'admin/',
        views.admin_notifications,
        name='admin_notifications'
    ),

    # AJAX GET
    path(
        '',
        views.get_notifications,
        name='get_notifications'
    ),

    # MARK SINGLE
    path(
        'read/<int:notif_id>/',
        views.mark_notification_read,
        name='mark_notification_read'
    ),

    # MARK ALL
    path(
        'read-all/',
        views.mark_all_read,
        name='mark_all_read'
    ),
    path(
    'clear/',
    views.clear_notifications,
    name='clear_notifications'
    ),
]

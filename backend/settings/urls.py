from django.urls import path
from . import views

urlpatterns = [

    # MAIN SETTINGS
    path(
        '',
        views.settings_page,
        name='settings_page'
    ),

    path(
        'admin/profile/',
        views.admin_profile,
        name='admin_profile'
    ),

    path(
        'admin/settings/',
        views.admin_settings,
        name='admin_settings'
    ),

    # TRAINER SETTINGS
    path(
        'trainer/',
        views.trainer_settings,
        name='trainer_settings'
    ),

    # STUDENT SETTINGS
    path(
        'student/',
        views.student_settings,
        name='student_settings'
    ),

]

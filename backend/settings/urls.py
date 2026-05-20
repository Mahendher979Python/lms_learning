from django.urls import path
from django.views.generic.base import RedirectView
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

    # TRAINER PROFILE & SETTINGS
    path(
        'trainer/',
        RedirectView.as_view(pattern_name='trainer_profile', permanent=True),
        name='trainer_old_redirect'
    ),
    
    path(
        'trainer/profile/',
        views.trainer_profile,
        name='trainer_profile'
    ),
    
    path(
        'trainer/settings/',
        views.trainer_settings,
        name='trainer_settings'
    ),

    # STUDENT PROFILE & SETTINGS
    path(
        'student/',
        RedirectView.as_view(pattern_name='student_profile', permanent=True),
        name='student_old_redirect'
    ),
    
    path(
        'student/profile/',
        views.student_profile,
        name='student_profile'
    ),
    
    path(
        'student/settings/',
        views.student_settings,
        name='student_settings'
    ),

]

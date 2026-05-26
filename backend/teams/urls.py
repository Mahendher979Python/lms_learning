from django.urls import path

from .views import (
    course_slides,
    course_teams,
    create_team,
    delete_message,
    get_students,
    messages_hub,
    notifications,
    react_message,
    request_dm,
    respond_dm_request,
    search,
    student_course_slides,
    trainer_course_slides,
    video_call,
)

app_name = 'teams'

urlpatterns = [
    path('messages/', messages_hub, name='messages_hub'),
    path('courses/', course_slides, name='course_slides'),
    path('course/<int:course_id>/', course_teams, name='course_teams'),
    path('create/<int:course_id>/', create_team, name='create_team'),
    path('search/', search, name='search'),
    path('get-students/', get_students, name='get_students'),
    path('notifications/', notifications, name='notifications'),
    path('delete-message/<int:msg_id>/', delete_message, name='delete_message'),
    path('react-message/<int:msg_id>/', react_message, name='react_message'),
    path(
    'trainer-courses/',
    trainer_course_slides,
    name='trainer_course_slides'
),

path(
    'student-courses/',
    student_course_slides,
    name='student_course_slides'
),
path(
    'video-call/<int:team_id>/',
    video_call,
    name='video_call'
),

    path('request-dm/<int:user_id>/', request_dm, name='request_dm'),
    path('respond-dm/<int:request_id>/', respond_dm_request, name='respond_dm_request'),

]

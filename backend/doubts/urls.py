from django.urls import path

from .views import (
    ask_course_bot,
    course_doubts,
    doubts_courses,
    invite_to_ticket,
    respond_ticket_invite,
    ticket_detail,
)

app_name = 'doubts'

urlpatterns = [
    path('courses/', doubts_courses, name='courses'),
    path('course/<int:course_id>/', course_doubts, name='course_doubts'),
    path('ticket/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/invite/', invite_to_ticket, name='invite_to_ticket'),
    path('invite/<int:invite_id>/respond/', respond_ticket_invite, name='respond_ticket_invite'),
    path('course/<int:course_id>/bot/ask/', ask_course_bot, name='ask_course_bot'),
]

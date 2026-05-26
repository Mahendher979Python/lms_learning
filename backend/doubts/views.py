import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

import google.generativeai as genai

from courses.models import Course

from .models import (
    CourseBotConversation,
    CourseBotMessage,
    DoubtTicket,
    DoubtTicketInvite,
    DoubtTicketMessage,
    DoubtTicketParticipant,
)


logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def _user_can_access_course(user, course):
    if user.role == 'admin':
        return True
    if user.role == 'trainer':
        return course.trainer_id == user.id
    if user.role == 'student':
        return course.students.filter(id=user.id).exists()
    return False


def _course_template_for_user(user):
    if user.role == 'admin':
        return 'doubts/admin_course_doubts.html'
    if user.role == 'trainer':
        return 'doubts/trainer_course_doubts.html'
    return 'doubts/student_course_doubts.html'


def _ticket_template_for_user(user):
    if user.role == 'admin':
        return 'doubts/admin_ticket_detail.html'
    if user.role == 'trainer':
        return 'doubts/trainer_ticket_detail.html'
    return 'doubts/student_ticket_detail.html'


def _courses_template_for_user(user):
    if user.role == 'admin':
        return 'doubts/admin_courses.html'
    if user.role == 'trainer':
        return 'doubts/trainer_courses.html'
    return 'doubts/student_courses.html'


@login_required
@require_http_methods(["GET"])
def doubts_courses(request):
    user = request.user
    if user.role == 'admin':
        courses = Course.objects.all()
    elif user.role == 'trainer':
        courses = Course.objects.filter(trainer=user)
    elif user.role == 'student':
        courses = Course.objects.filter(students=user)
    else:
        courses = Course.objects.none()

    return render(request, _courses_template_for_user(user), {
        'courses': courses,
    })


@login_required
@require_http_methods(["GET", "POST"])
def course_doubts(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not _user_can_access_course(request.user, course):
        return redirect('teams:course_slides')

    conversation, _ = CourseBotConversation.objects.get_or_create(course=course)

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        initial_message = (request.POST.get("initial_message") or "").strip()

        if title:
            ticket = DoubtTicket.objects.create(
                course=course,
                title=title,
                created_by=request.user,
                status='open'
            )
            DoubtTicketParticipant.objects.get_or_create(ticket=ticket, user=request.user)

            if initial_message:
                DoubtTicketMessage.objects.create(
                    ticket=ticket,
                    sender=request.user,
                    sender_name=request.user.username,
                    content=initial_message
                )

            return redirect('doubts:ticket_detail', ticket_id=ticket.id)

    if request.user.role in ['admin', 'trainer']:
        tickets = DoubtTicket.objects.filter(course=course)
    else:
        tickets = DoubtTicket.objects.filter(course=course).filter(
            models.Q(created_by=request.user)
            | models.Q(participants=request.user)
            | models.Q(assigned_to=request.user)
        ).distinct()

    invites_received = DoubtTicketInvite.objects.filter(
        invited_user=request.user,
        status='pending',
        ticket__course=course
    ).select_related('ticket', 'invited_by')

    bot_messages = conversation.messages.select_related('sender').all()

    return render(request, _course_template_for_user(request.user), {
        'course': course,
        'tickets': tickets,
        'invites_received': invites_received,
        'bot_messages': bot_messages,
    })


@login_required
@require_http_methods(["GET", "POST"])
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(DoubtTicket, id=ticket_id)
    course = ticket.course

    if not _user_can_access_course(request.user, course):
        return redirect('teams:course_slides')

    is_participant = ticket.participants.filter(id=request.user.id).exists() or ticket.created_by_id == request.user.id
    is_invited = ticket.invites.filter(invited_user=request.user, status='pending').exists()

    if request.user.role == 'student' and not (is_participant or is_invited):
        return redirect('doubts:course_doubts', course_id=course.id)

    if request.method == "POST":
        content = (request.POST.get("message") or "").strip()
        if content and is_participant:
            DoubtTicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                sender_name=request.user.username,
                content=content
            )
            return redirect('doubts:ticket_detail', ticket_id=ticket.id)

        if request.POST.get("close_ticket") and (request.user.role in ['admin', 'trainer'] or ticket.created_by_id == request.user.id):
            ticket.status = 'closed'
            ticket.save()
            return redirect('doubts:ticket_detail', ticket_id=ticket.id)

    messages = ticket.messages.select_related('sender').all()
    participants = ticket.participants.all()
    invites = ticket.invites.select_related('invited_by', 'invited_user').all()

    inviteable_users = []
    if request.user.role in ['admin', 'trainer'] or is_participant:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        inviteable_users = User.objects.filter(
            models.Q(id__in=course.students.values_list('id', flat=True))
            | models.Q(id=course.trainer_id)
            | models.Q(role='admin')
        ).exclude(id__in=participants.values_list('id', flat=True)).distinct()

    return render(request, _ticket_template_for_user(request.user), {
        'course': course,
        'ticket': ticket,
        'messages': messages,
        'participants': participants,
        'invites': invites,
        'inviteable_users': inviteable_users,
        'is_participant': is_participant,
    })


@login_required
@require_http_methods(["POST"])
def invite_to_ticket(request, ticket_id):
    ticket = get_object_or_404(DoubtTicket, id=ticket_id)
    course = ticket.course

    if not _user_can_access_course(request.user, course):
        return redirect('teams:course_slides')

    is_participant = ticket.participants.filter(id=request.user.id).exists() or ticket.created_by_id == request.user.id
    if not (request.user.role in ['admin', 'trainer'] or is_participant):
        return redirect('doubts:ticket_detail', ticket_id=ticket.id)

    invited_user_id = request.POST.get('invited_user_id')
    if invited_user_id:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        invited_user = get_object_or_404(User, id=invited_user_id)

        DoubtTicketInvite.objects.update_or_create(
            ticket=ticket,
            invited_user=invited_user,
            defaults={
                'invited_by': request.user,
                'status': 'pending',
                'responded_at': None,
            }
        )

    return redirect('doubts:ticket_detail', ticket_id=ticket.id)


@login_required
@require_http_methods(["POST"])
def respond_ticket_invite(request, invite_id):
    invite = get_object_or_404(DoubtTicketInvite, id=invite_id)
    if invite.invited_user_id != request.user.id:
        return redirect('doubts:course_doubts', course_id=invite.ticket.course_id)

    action = request.POST.get('action')
    if invite.status == 'pending' and action in ['accept', 'decline']:
        invite.status = 'accepted' if action == 'accept' else 'declined'
        invite.responded_at = timezone.now()
        invite.save()

        if invite.status == 'accepted':
            DoubtTicketParticipant.objects.get_or_create(ticket=invite.ticket, user=request.user)

    return redirect('doubts:ticket_detail', ticket_id=invite.ticket.id)


@login_required
@require_http_methods(["POST"])
def ask_course_bot(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not _user_can_access_course(request.user, course):
        return JsonResponse({"error": "Not allowed"}, status=403)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        data = {}

    message = (data.get("message") or "").strip()
    if not message:
        return JsonResponse({"error": "Message is required"}, status=400)

    conversation, _ = CourseBotConversation.objects.get_or_create(course=course)

    user_message = CourseBotMessage.objects.create(
        conversation=conversation,
        role='user',
        sender=request.user,
        content=message
    )

    messages_history = CourseBotMessage.objects.filter(conversation=conversation).order_by('created_at')
    chat_history = [{"role": msg.role, "parts": [msg.content]} for msg in messages_history]

    try:
        response = model.generate_content(chat_history)
        ai_response = response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        logger.error(f"AI Error: {str(e)}")
        return JsonResponse({"error": f"AI Error: {str(e)}"}, status=500)

    ai_message = CourseBotMessage.objects.create(
        conversation=conversation,
        role='assistant',
        content=ai_response
    )

    user_message.tokens_used = len(message.split())
    user_message.save()
    ai_message.tokens_used = len(ai_response.split())
    ai_message.save()

    conversation.updated_at = timezone.now()
    conversation.save()

    return JsonResponse({
        "reply": ai_response,
        "user_message_id": user_message.id,
        "ai_message_id": ai_message.id,
    })

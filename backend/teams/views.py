from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q, Max
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from notifications.models import Notification  # FIXED IMPORT

from .models import Team, Message, PrivateMessage, Reaction, PrivateChatRequest
from .forms import TeamForm
from courses.models import Course

User = get_user_model()


# =========================
# COURSE SLIDES (MAIN)
# =========================
@login_required
def course_slides(request):
    user = request.user

    if user.role == 'admin':
        courses = Course.objects.all()
        template = 'teams/course_slides.html'

    elif user.role == 'trainer':
        courses = Course.objects.filter(trainer=user)
        template = 'teams/trainer_course_slides.html'

    elif user.role == 'student':
        courses = Course.objects.filter(students=user)
        template = 'teams/student_course_slides.html'

    else:
        return redirect('/')

    return render(request, template, {'courses': courses})


# =========================
# TRAINER COURSE SLIDES (FIXED)
# =========================
@login_required
def trainer_course_slides(request):
    if request.user.role != 'trainer':
        return redirect('teams:course_slides')

    courses = Course.objects.filter(trainer=request.user)

    return render(
        request,
        'teams/trainer_course_slides.html',
        {'courses': courses}
    )


# =========================
# STUDENT COURSE SLIDES
# =========================
@login_required
def student_course_slides(request):
    if request.user.role != 'student':
        return redirect('teams:course_slides')

    courses = Course.objects.filter(students=request.user)

    return render(
        request,
        'teams/student_course_slides.html',
        {'courses': courses}
    )


def _messages_template_for_user(user):
    if user.role == 'admin':
        return 'teams/admin_messages.html'
    if user.role == 'trainer':
        return 'teams/trainer_messages.html'
    return 'teams/student_messages.html'


@login_required
@require_http_methods(["GET", "POST"])
def messages_hub(request):
    user = request.user
    user_id = request.GET.get('user_id')

    selected_user = None
    private_messages = []

    if user_id:
        selected_user = get_object_or_404(User, id=user_id)

    if request.method == "POST" and selected_user:
        msg = (request.POST.get("message") or "").strip()
        uploaded_file = request.FILES.get("file")
        if msg or uploaded_file:
            PrivateMessage.objects.create(
                sender=user,
                receiver=selected_user,
                message=msg,
                file=uploaded_file
            )
            return redirect(f"{request.path}?user_id={selected_user.id}")

    users = User.objects.exclude(id=user.id).filter(
        role__in=['admin', 'trainer', 'student']
    ).order_by('username')

    recent_users = User.objects.filter(
        Q(sent_pm__receiver=user) |
        Q(received_pm__sender=user)
    ).distinct().order_by('username')

    if selected_user:
        private_messages = PrivateMessage.objects.filter(
            Q(sender=user, receiver=selected_user) |
            Q(sender=selected_user, receiver=user)
        ).order_by('timestamp')

    return render(request, _messages_template_for_user(user), {
        'users': users,
        'recent_users': recent_users,
        'selected_user': selected_user,
        'private_messages': private_messages,
    })


# =========================
# COURSE TEAMS + CHAT
# =========================
@login_required
def course_teams(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    if user.role == 'admin':
        teams = Team.objects.filter(course=course)

    elif user.role == 'trainer':
        teams = Team.objects.filter(course=course, trainer=user)

    elif user.role == 'student':
        teams = Team.objects.filter(course=course, students=user)

    else:
        teams = Team.objects.none()

    teams = teams.annotate(
        last_msg_time=Max('messages__timestamp')
    ).order_by('-last_msg_time')

    trainers = User.objects.filter(role='trainer')

    team_id = request.GET.get('team_id')
    user_id = request.GET.get('user_id')

    team = None
    selected_user = None
    messages = []
    private_messages = []

    recent_users = User.objects.filter(
        Q(sent_pm__receiver=user) |
        Q(received_pm__sender=user)
    ).distinct()

    notifications = Notification.objects.filter(
        recipient=user,
        is_read=False
    )

    dm_requests_received = PrivateChatRequest.objects.filter(
        recipient=user,
        status='pending'
    ).select_related('requester')

    dm_requests_sent = PrivateChatRequest.objects.filter(
        requester=user,
        status='pending'
    ).select_related('recipient')

    # GROUP CHAT
    if team_id:
        team = get_object_or_404(Team, id=team_id)

        if user.role == 'trainer' and team.trainer != user:
            return redirect('teams:course_slides')

        if user.role == 'student' and user not in team.students.all():
            return redirect('teams:course_slides')

        messages = Message.objects.filter(team=team).order_by('timestamp')

    # PRIVATE CHAT
    if user_id:
        selected_user = get_object_or_404(User, id=user_id)

        private_messages = PrivateMessage.objects.filter(
            Q(sender=user, receiver=selected_user) |
            Q(sender=selected_user, receiver=user)
        ).order_by('timestamp')

    dm_request = None
    dm_allowed = False
    if selected_user:
        dm_request = PrivateChatRequest.objects.filter(
            Q(requester=user, recipient=selected_user) |
            Q(requester=selected_user, recipient=user)
        ).first()

        dm_allowed = True

    # SEND MESSAGE
    if request.method == 'POST':
        msg = request.POST.get('message') or request.POST.get('private_message')
        uploaded_file = request.FILES.get('file')

        reply_id = request.POST.get('reply_id')
        reply_obj = Message.objects.filter(id=reply_id).first() if reply_id else None

        # GROUP MESSAGE
        if team and (msg or uploaded_file):
            Message.objects.create(
                team=team,
                sender=user,
                content=msg or "",
                file=uploaded_file,
                reply_to=reply_obj
            )

        # PRIVATE MESSAGE
        elif selected_user and (msg or uploaded_file):
            PrivateMessage.objects.create(
                sender=user,
                receiver=selected_user,
                message=msg or "",
                file=uploaded_file
            )

        if team_id:
            return redirect(f"{request.path}?team_id={team_id}")
        elif user_id:
            return redirect(f"{request.path}?user_id={user_id}")

        return redirect(request.path)

    return render(request, 'teams/course_teams.html', {
        'course': course,
        'teams': teams,
        'team': team,
        'messages': messages,
        'private_messages': private_messages,
        'selected_user': selected_user,
        'recent_users': recent_users,
        'notifications': notifications,
        'dm_requests_received': dm_requests_received,
        'dm_requests_sent': dm_requests_sent,
        'dm_request': dm_request,
        'dm_allowed': dm_allowed,
        'trainers': trainers,
    })


# =========================
# CREATE TEAM
# =========================
@login_required
def create_team(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = TeamForm(request.POST or None)

    if form.is_valid():
        team = form.save(commit=False)
        team.course = course
        team.save()
        form.save_m2m()
        return redirect('teams:course_teams', course_id=course.id)

    return render(request, 'teams/create_team.html', {'form': form})


# =========================
# GET STUDENTS (AJAX)
# =========================
@login_required
def get_students(request):
    trainer_id = request.GET.get('trainer_id')

    students = User.objects.filter(
        role='student',
        trainer_id=trainer_id
    ).values('id', 'username')

    return JsonResponse(list(students), safe=False)


# =========================
# NOTIFICATIONS
# =========================
@login_required
def notifications(request):
    notes = Notification.objects.filter(recipient=request.user)
    return render(request, 'teams/notifications.html', {'notes': notes})


# =========================
# SEARCH
# =========================
@login_required
def search(request):
    query = request.GET.get('q', '')

    users = User.objects.filter(username__icontains=query)
    teams = Team.objects.filter(name__icontains=query)

    return render(request, 'teams/search.html', {
        'users': users,
        'teams': teams,
        'query': query
    })


# =========================
# DELETE MESSAGE
# =========================
@login_required
def delete_message(request, msg_id):
    msg = get_object_or_404(Message, id=msg_id)

    if request.user == msg.sender or request.user.role == "admin":
        msg.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "not allowed"}, status=403)


# =========================
# REACT MESSAGE
# =========================
@login_required
def react_message(request, msg_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    emoji = request.POST.get("emoji")
    if not emoji:
        return JsonResponse({"error": "emoji missing"}, status=400)

    msg = get_object_or_404(Message, id=msg_id)

    reaction, created = Reaction.objects.get_or_create(
        message=msg,
        user=request.user,
        defaults={"emoji": emoji}
    )

    if not created:
        reaction.emoji = emoji
        reaction.save()

    return JsonResponse({"success": True, "emoji": reaction.emoji})


# =========================
# VIDEO CALL
# =========================
@login_required
def video_call(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    user = request.user

    allowed = (
        user.role == 'admin'
        or (user.role == 'trainer' and team.trainer == user)
        or (user.role == 'student' and user in team.students.all())
    )

    if not allowed:
        return redirect('teams:course_slides')

    notifications = Notification.objects.filter(
        recipient=user,
        is_read=False
    ).order_by('-created_at')

    return render(request, 'teams/video_call.html', {
        'team': team,
        'notifications': notifications
    })


@login_required
@require_http_methods(["POST"])
def request_dm(request, user_id):
    recipient = get_object_or_404(User, id=user_id)
    if recipient.id == request.user.id:
        return JsonResponse({"error": "invalid"}, status=400)

    req, _ = PrivateChatRequest.objects.update_or_create(
        requester=request.user,
        recipient=recipient,
        defaults={
            "status": "pending",
            "responded_at": None,
        }
    )

    return JsonResponse({"success": True, "request_id": req.id})


@login_required
@require_http_methods(["POST"])
def respond_dm_request(request, request_id):
    req = get_object_or_404(PrivateChatRequest, id=request_id)
    if req.recipient_id != request.user.id:
        return JsonResponse({"error": "not allowed"}, status=403)

    action = request.POST.get("action")
    if req.status == "pending" and action in ["accept", "decline"]:
        req.status = "accepted" if action == "accept" else "declined"
        req.responded_at = timezone.now()
        req.save()

    return JsonResponse({"success": True, "status": req.status})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Notification

# =====================================================
# STUDENT NOTIFICATIONS
# =====================================================
@login_required
def student_notifications(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    notifications.update(is_read=True)

    all_read = not notifications.filter(
        is_read=False
    ).exists()

    return render(
        request,
        'notifications/student_notifications.html',
        {
            'notifications': notifications,
            'all_read': all_read
        }
    )

# =====================================================
# TRAINER NOTIFICATIONS
# =====================================================
@login_required
def trainer_notifications(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    notifications.update(is_read=True)

    all_read = not notifications.filter(
        is_read=False
    ).exists()

    return render(
        request,
        'notifications/trainer_notifications.html',
        {
            'notifications': notifications,
            'all_read': all_read
        }
    )

# =====================================================
# ADMIN NOTIFICATIONS
# =====================================================
@login_required
def admin_notifications(request):

    if request.user.role != "admin":
        return redirect("login")

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    notifications.update(is_read=True)

    all_read = not notifications.filter(
        is_read=False
    ).exists()

    return render(
        request,
        'notifications/admin_notifications.html',
        {
            'notifications': notifications,
            'all_read': all_read
        }
    )
# =====================================================
# AJAX GET NOTIFICATIONS
# =====================================================

@login_required
def get_notifications(request):

    notifications_qs = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    unread_count = notifications_qs.filter(
        is_read=False
    ).count()

    notifications = notifications_qs[:10]

    data = {

        "unread_count": unread_count,

        "notifications": [

            {
                "id": n.id,
                "type": n.type,
                "message": n.message,
                "course": n.course_name or "",
                "time": n.created_at.strftime(
                    "%d %b %Y %I:%M %p"
                ),
                "is_read": n.is_read
            }

            for n in notifications
        ]
    }

    return JsonResponse(data)


# =====================================================
# MARK SINGLE READ
# =====================================================

@login_required
@require_POST
def mark_notification_read(request, notif_id):

    try:

        notif = Notification.objects.get(
            id=notif_id,
            recipient=request.user
        )

        notif.is_read = True

        notif.save()

        return JsonResponse({
            "status": "success"
        })

    except Notification.DoesNotExist:

        return JsonResponse({
            "status": "error"
        })

# =====================================================
# MARK ALL READ
# =====================================================

@login_required
@require_POST
def mark_all_read(request):

    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({
        "status": "success"
    })


# =====================================================
# CLEAR ALL NOTIFICATIONS
# =====================================================
@login_required
@require_POST
def clear_notifications(request):

    Notification.objects.filter(
        recipient=request.user,
        is_read=True
    ).delete()

    return JsonResponse({
        "status": "success"
    })
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Q
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from datetime import timedelta
import base64
import requests
import csv
from django.http import HttpResponse
from accounts.models import User
from .models import Attendance, Break, LocationLog


def _trainer_students(trainer_user):
    if getattr(trainer_user, "role", None) != "trainer":
        return User.objects.none()
    return (
        User.objects.filter(role="student")
        .filter(Q(trainer=trainer_user) | Q(enrolled_courses__trainer=trainer_user))
        .distinct()
    )


def _get_or_create_attendance(user, date):
    attendance = Attendance.objects.filter(user=user, date=date).order_by("-id").first()
    if attendance:
        return attendance, False
    return Attendance.objects.create(user=user, date=date), True


# =========================
# STUDENT ATTENDANCE
# =========================
@login_required
def student_attendance(request):
    today = timezone.localdate()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()
    records = Attendance.objects.filter(user=request.user).order_by('-date')

    chart_data = Attendance.objects.filter(user=request.user).values('date').annotate(
        total=Sum('total_hours')).order_by('date')
    dates = [str(d['date']) for d in chart_data]
    hours = [float(d['total'] or 0) for d in chart_data]

    week_start  = today - timedelta(days=7)
    month_start = today.replace(day=1)
    year_start  = today.replace(month=1, day=1)

    daily_hours   = Attendance.objects.filter(user=request.user, date=today).aggregate(Sum('total_hours'))['total_hours__sum'] or 0
    weekly_hours  = Attendance.objects.filter(user=request.user, date__gte=week_start).aggregate(Sum('total_hours'))['total_hours__sum'] or 0
    monthly_hours = Attendance.objects.filter(user=request.user, date__gte=month_start).aggregate(Sum('total_hours'))['total_hours__sum'] or 0
    yearly_hours  = Attendance.objects.filter(user=request.user, date__gte=year_start).aggregate(Sum('total_hours'))['total_hours__sum'] or 0

    context = {
        "attendance":        attendance,
        # ✅ FIX: today_logout_time was missing — timer never stopped without it
        "today_login_time":  attendance.login_time.isoformat()  if attendance and attendance.login_time  else "",
        "today_logout_time": attendance.logout_time.isoformat() if attendance and attendance.logout_time else "",
        "records":           records,
        "daily_hours":       daily_hours,
        "weekly_hours":      weekly_hours,
        "monthly_hours":     monthly_hours,
        "yearly_hours":      yearly_hours,
        "dates":             json.dumps(dates),
        "hours":             json.dumps(hours),
    }
    return render(request, "attendance/student_attendance.html", context)


# =========================
# TRAINER ATTENDANCE
# =========================
@login_required
def trainer_attendance(request):
    if request.user.role != "trainer":
        return redirect("student_attendance")
    get_token(request)
    today = timezone.localdate()
    attendance = Attendance.objects.filter(user=request.user, date=today).first()
    trainer_records = Attendance.objects.filter(user=request.user).order_by('-date')
    students = _trainer_students(request.user)
    student_records = Attendance.objects.filter(user__in=students).select_related("user").order_by("-date", "-id")

    total_students = students.count()
    present_today  = Attendance.objects.filter(user__in=students, date=today, login_time__isnull=False).values("user").distinct().count()
    absent_today   = total_students - present_today
    dates = [str(r.date) for r in trainer_records]
    hours = [float(r.total_hours or 0) for r in trainer_records]

    today_login_time  = attendance.login_time.isoformat()  if attendance and attendance.login_time  else ""
    today_logout_time = attendance.logout_time.isoformat() if attendance and attendance.logout_time else ""

    latest_lat    = float(attendance.latitude  or 0) if attendance else 0
    latest_lng    = float(attendance.longitude or 0) if attendance else 0
    location_name = attendance.location_name if attendance and attendance.location_name else ""

    context = {
        'trainer_records':   trainer_records,
        'student_records':   student_records,
        'attendance':        attendance,
        'dates_json':        json.dumps(dates),
        'hours_json':        json.dumps(hours),
        'today_login_time':  today_login_time,
        'today_logout_time': today_logout_time,
        'total_students':    total_students,
        'present_today':     present_today,
        'absent_today':      absent_today,
        'latest_lat':        latest_lat,
        'latest_lng':        latest_lng,
        'location_name':     location_name,
    }
    return render(request, 'attendance/trainer_attendance.html', context)


# =========================
# SINGLE STUDENT VIEW
# =========================
@login_required
def student_attendance_view(request, user_id):
    if request.user.role != "trainer":
        return redirect("student_attendance")
    student = get_object_or_404(User, id=user_id)
    if not _trainer_students(request.user).filter(id=student.id).exists():
        return redirect("assigned_students")
    records = Attendance.objects.filter(user=student).order_by('-date')
    chart_data = Attendance.objects.filter(user=student).values('date').annotate(
        total=Sum('total_hours')).order_by('date')
    dates = [str(d['date']) for d in chart_data]
    hours = [float(d['total'] or 0) for d in chart_data]
    return render(request, "attendance/student_attendance_view.html", {
        "student": student,
        "records": records,
        "dates":   json.dumps(dates),
        "hours":   json.dumps(hours),
    })


# =========================
# LOGIN ATTENDANCE (with location)
# =========================
@login_required
def login_time(request):
    today = timezone.localdate()
    attendance, created = _get_or_create_attendance(request.user, today)

    # Set login_time if not already clocked in
    if not attendance.login_time:
        attendance.login_time  = timezone.now()
        attendance.logout_time = None
        attendance.status      = "Present"
    
    # Always save attendance (even if login was already set)
    attendance.save()

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat  = data.get("lat")
            lng  = data.get("lng")
            if lat and lng:
                place = get_location_name(lat, lng)
                attendance.latitude      = lat
                attendance.longitude     = lng
                attendance.location_name = place
                attendance.save()

                LocationLog.objects.create(
                    user=request.user,
                    latitude=lat,
                    longitude=lng
                )
                return JsonResponse({"status": "success", "location": place})
            else:
                return JsonResponse({"status": "success", "location": ""})
        except Exception:
            return JsonResponse({"status": "success", "location": ""})

    if request.user.role == "trainer":
        return redirect('trainer_attendance')
    return redirect('student_attendance')


# =========================
# LOGOUT ATTENDANCE
# =========================
@login_required
def logout_time(request):
    today = timezone.localdate()
    attendance = Attendance.objects.filter(user=request.user, date=today).order_by("-id").first()

    if attendance and not attendance.logout_time:
        attendance.logout_time = timezone.now()
        if attendance.login_time:
            diff        = attendance.logout_time - attendance.login_time
            hours       = diff.total_seconds() / 3600
            final_hours = round(hours - float(attendance.break_hours or 0), 2)
            attendance.total_hours = final_hours
            attendance.status = "Present"
        attendance.save()

    if request.user.role == "trainer":
        return redirect('trainer_attendance')
    return redirect('student_attendance')


# =========================
# WEBSITE LOGOUT
# =========================
@csrf_exempt
@login_required
def logout_attendance(request):
    today = timezone.localdate()
    attendance = Attendance.objects.filter(user=request.user, date=today).order_by("-id").first()

    if attendance and not attendance.logout_time:
        attendance.logout_time = timezone.now()
        if attendance.login_time:
            diff = attendance.logout_time - attendance.login_time
            hours = diff.total_seconds() / 3600
            attendance.total_hours = round(hours - float(attendance.break_hours or 0), 2)
            attendance.status = "Present"
        attendance.save()

    logout(request)
    return redirect("login")


# =========================
# BREAK START
# =========================
@login_required
def start_break(request):
    today = timezone.localdate()
    attendance = Attendance.objects.filter(user=request.user, date=today).order_by("-id").first()
    if not attendance or not attendance.login_time or attendance.logout_time:
        return JsonResponse({"status": "not_checked_in"}, status=400)
    if attendance.break_start:
        return JsonResponse({"status": "already_on_break"}, status=400)
    attendance.break_start = timezone.now()
    attendance.save()
    return JsonResponse({"status": "break_started"})


# =========================
# BREAK END
# =========================
@login_required
def end_break(request):
    today = timezone.localdate()
    attendance = Attendance.objects.filter(user=request.user, date=today).order_by("-id").first()
    if not attendance or not attendance.break_start:
        return JsonResponse({"status": "no_active_break"}, status=400)
    if attendance.break_start:
        diff = timezone.now() - attendance.break_start
        attendance.break_hours += diff.total_seconds() / 3600
        attendance.break_end   = timezone.now()
        attendance.break_start = None
        attendance.save()
    return JsonResponse({"status": "break_ended"})


# =========================
# LOCATION NAME (Nominatim - Free)
# =========================
def get_location_name(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, headers={'User-Agent': 'lms-attendance-app'})
        data = response.json()
        return data.get('display_name', 'Unknown Location')
    except Exception:
        return "Location not found"


# =========================
# AUTO LOCATION
# =========================
@login_required
def auto_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            data = {}
        lat = data.get("lat")
        lng = data.get("lng")
        today = timezone.localdate()
        attendance = Attendance.objects.filter(user=request.user, date=today).order_by("-id").first()
        if attendance and lat and lng:
            place = get_location_name(lat, lng)
            attendance.latitude      = lat
            attendance.longitude     = lng
            attendance.location_name = place
            attendance.save()
        return JsonResponse({"status": "ok"})


# =========================
# TRACK LOCATION
# =========================
@login_required
def track_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            data = {}
        LocationLog.objects.create(
            user=request.user,
            latitude=data.get("lat"),
            longitude=data.get("lng")
        )
        return JsonResponse({"status": "ok"})


# =========================
# LATEST LOCATION
# =========================
@login_required
def latest_location(request):
    attendance = Attendance.objects.filter(user=request.user).order_by('-id').first()
    if attendance:
        return JsonResponse({
            "lat":           float(attendance.latitude  or 0),
            "lng":           float(attendance.longitude or 0),
            "location_name": attendance.location_name or ""
        })
    return JsonResponse({"lat": 0, "lng": 0, "location_name": ""})


# =========================
# FACE ATTENDANCE
# =========================
@login_required
def face_attendance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            data = {}
        image_data = data.get("image")
        if image_data:
            format, imgstr = image_data.split(';base64,')
            file = ContentFile(base64.b64decode(imgstr), name=f"{request.user.username}.png")
            today = timezone.localdate()
            attendance, created = _get_or_create_attendance(request.user, today)
            if not attendance.login_time:
                attendance.login_time = timezone.now()
            attendance.image = file
            attendance.save()
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "failed"})
    return JsonResponse({"status": "invalid"})

# =========================
# USER LOCATION (admin — fetch any user's latest location)
# =========================
@login_required
def user_location(request, user_id):
    user = get_object_or_404(User, id=user_id)
    attendance = Attendance.objects.filter(user=user).order_by('-date', '-id').first()
    if attendance and attendance.latitude:
        return JsonResponse({
            "lat":           float(attendance.latitude),
            "lng":           float(attendance.longitude),
            "location_name": attendance.location_name or "",
            "username":      user.username,
            "date":          str(attendance.date),
        })
    return JsonResponse({
        "lat": 0, "lng": 0,
        "location_name": "",
        "username": user.username,
        "date": "",
    })


# =========================
# ATTENDANCE DATA
# =========================
@login_required
def attendance_data(request):
    data = [{"date": str(r.date), "hours": r.total_hours}
            for r in Attendance.objects.filter(user=request.user)]
    return JsonResponse(data, safe=False)


# =========================
# ATTENDANCE PREDICTION
# =========================
@login_required
def attendance_prediction(request):
    records = Attendance.objects.filter(user=request.user)
    total   = records.count()
    present = records.filter(login_time__isnull=False).count()
    percent = (present / total * 100) if total else 0
    return JsonResponse({
        "attendance_percentage": round(percent, 2),
        "status": "Good" if percent > 75 else "Low"
    })


# =========================
# ASSIGNED STUDENTS
# =========================
@login_required
def assigned_students(request):
    if request.user.role != "trainer":
        return redirect("student_attendance")
    students = _trainer_students(request.user)
    return render(request, "attendance/assigned_students.html", {"students": students})


# =========================
# STUDENT DETAIL
# =========================
@login_required
def student_detail_attendance(request, user_id):
    student = get_object_or_404(User, id=user_id)
    records = Attendance.objects.filter(user=student).order_by('-date')
    return render(request, "attendance/student_detail.html", {"student": student, "records": records})


# =========================
# ADMIN ATTENDANCE
# =========================
@login_required
def admin_attendance(request):
    records = Attendance.objects.all().order_by('-date')
    date = request.GET.get('date')
    user = request.GET.get('user')
    if date: records = records.filter(date=date)
    if user: records = records.filter(user__username__icontains=user)

    today         = timezone.localdate()
    total_users   = User.objects.count()
    present_today = Attendance.objects.filter(date=today).values('user').distinct().count()
    absent_today  = total_users - present_today

    chart_records = Attendance.objects.all().order_by('date')
    dates = [r.date.strftime("%d-%m") for r in chart_records]
    hours = [float(r.total_hours or 0) for r in chart_records]

    return render(request, 'attendance/admin_attendance.html', {
        'records':       records,
        'total_users':   total_users,
        'present_today': present_today,
        'absent_today':  absent_today,
        'dates':         json.dumps(dates),
        'hours':         json.dumps(hours),
    })



@login_required
def export_attendance_csv(request):
    user = request.user
    scope = request.GET.get('scope', 'self')  # options: 'self', 'students', 'admin_all'
    
    # Base Queryset
    records = Attendance.objects.all()

    # Permission-based filtering
    if scope == 'admin_all':
        # Apply filters from Admin Dashboard
        date_query = request.GET.get('date')
        user_query = request.GET.get('user')
        if date_query:
            records = records.filter(date=date_query)
        if user_query:
            records = records.filter(user__username__icontains=user_query)
    elif scope == 'students' and user.role == 'trainer':
        records = records.filter(user__in=_trainer_students(user))
    else:
        # Default: Export current user's own records
        records = records.filter(user=user)

    records = records.order_by('-date', '-login_time')

    # Create CSV Response
    response = HttpResponse(content_type='text/csv')
    filename = f"attendance_{scope}_{timezone.now().date()}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Date', 'Login Time', 'Logout Time', 'Work Hours', 'Break Hours', 'Status', 'Location'])

    for r in records:
        status = r.status or ("Present" if r.login_time else "Absent")
        writer.writerow([
            r.user.username,
            r.date,
            r.login_time.strftime("%H:%M:%S") if r.login_time else "-",
            r.logout_time.strftime("%H:%M:%S") if r.logout_time else "-",
            r.total_hours,
            round(r.break_hours, 2),
            status,
            r.location_name or "N/A"
        ])

    return response

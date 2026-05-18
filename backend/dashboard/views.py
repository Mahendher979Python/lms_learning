from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from courses.models import Course, Topic
from assignments.models import Assignment
from assignments.models import  Submission




@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("login")

    from accounts.models import User
    from courses.models import Course
    from assignments.models import Assignment

    trainers = User.objects.filter(role="trainer").count()
    students = User.objects.filter(role="student").count()
    courses = Course.objects.count()
    assignments = Assignment.objects.count()

    return render(request, "dashboard/admin_dashboard.html", {
        "trainers": trainers,
        "students": students,
        "courses": courses,
        "assignments": assignments,
    })
@login_required
def trainer_dashboard(request):

    # trainer profile
    trainer = request.user

    # USE request.user
    courses = Course.objects.filter(trainer=request.user)

    topics = Topic.objects.filter(
        course__trainer=request.user
    )

    assignments = Assignment.objects.filter(
        course__trainer=request.user
    )

    # STUDENT COUNT
    students_count = User.objects.filter(role="student").count()

    # PROGRESS
    for c in courses:

        # use topics instead of topic_set
        total_topics = c.topics.count()

        completed = total_topics // 2
        pending = total_topics - completed

        c.completed_topics = completed
        c.pending_topics = pending

        if total_topics > 0:
            c.progress = int(
                (completed / total_topics) * 100
            )
        else:
            c.progress = 0

    return render(
        request,
        'dashboard/trainer_dashboard.html',
        {
            'courses': courses,
            'topics': topics,
            'assignments': assignments,
            'students_count': students_count,
        }
    )
@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("login")

    student = request.user

    # ⭐ BEST WAY (SAFE + CLEAN)
    courses = Course.objects.filter(students=student)

    assignments = Assignment.objects.filter(course__in=courses)
    topics = Topic.objects.filter(course__in=courses)

    total_assignments = assignments.count()
    completed_assignments = assignments.filter(status="completed").count()

    progress_percent = int(
        (completed_assignments / total_assignments) * 100
    ) if total_assignments > 0 else 0

    return render(request, "dashboard/student_dashboard.html", {
        "student": student,
        "courses": courses,
        "assignments": assignments,
        "topics": topics,
        "total_courses": courses.count(),
        "total_assignments": total_assignments,
        "total_topics": topics.count(),
        "completed_assignments": completed_assignments,
        "progress_percent": progress_percent,
    })
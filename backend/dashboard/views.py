from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import User
from courses.models import Course, Topic
from assignments.models import Assignment, Submission
from certificates.models import Certificate
from progress.models import Progress


# =========================
# ADMIN DASHBOARD
# =========================
@login_required
def admin_dashboard(request):

    if request.user.role != "admin":
        return redirect("login")

    trainers = User.objects.filter(role="trainer").count()
    students = User.objects.filter(role="student").count()
    courses = Course.objects.count()
    assignments = Assignment.objects.count()

    return render(
        request,
        "dashboard/admin_dashboard.html",
        {
            "trainers": trainers,
            "students": students,
            "courses": courses,
            "assignments": assignments,
        }
    )


# =========================
# TRAINER DASHBOARD
# =========================
@login_required
def trainer_dashboard(request):

    if request.user.role != "trainer":
        return redirect("login")

    trainer = request.user

    # Trainer Courses
    courses = Course.objects.filter(trainer=trainer)

    # Topics
    topics = Topic.objects.filter(
        course__trainer=trainer
    )

    # Assignments
    assignments = Assignment.objects.filter(
        course__trainer=trainer
    )

    # Student Count
    students_count = User.objects.filter(
        role="student"
    ).count()

    # Course Progress
    for c in courses:

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
        "dashboard/trainer_dashboard.html",
        {
            "courses": courses,
            "topics": topics,
            "assignments": assignments,
            "students_count": students_count,
        }
    )


# =========================
# STUDENT DASHBOARD
# =========================
@login_required
def student_dashboard(request):

    if request.user.role != "student":
        return redirect("login")

    student = request.user

    # Student Courses
    courses = Course.objects.filter(
        students=student
    )

    # Assignments
    assignments = Assignment.objects.filter(
        course__in=courses
    )

    # Topics
    topics = Topic.objects.filter(
        course__in=courses
    )

    # =========================
    # OVERALL PROGRESS
    # =========================
    total_assignments = assignments.count()

    submissions = Submission.objects.filter(
        student=student,
        assignment__in=assignments,
        status__in=["submitted", "graded"],
    ).select_related("assignment")

    total_percent = 0.0

    for s in submissions:
        total_percent += float(
            getattr(s, "percentage", 0) or 0
        )

    progress_percent = (
        int(round(total_percent / total_assignments))
        if total_assignments > 0
        else 0
    )

    # =========================
    # CERTIFICATES
    # =========================
    certificates = Certificate.objects.filter(
        student=student,
        status="approved"
    ).count()

    # =========================
    # SAVED COURSE PROGRESS
    # =========================
    saved_progress = {
        p.course_id: p
        for p in Progress.objects.filter(
            student=student,
            course__in=courses
        ).select_related("course")
    }

    # =========================
    # COURSE-WISE PROGRESS
    # =========================
    for c in courses:

        p = saved_progress.get(c.id)

        if p is not None:
            c.progress = p.attendance or 0
            continue

        c_assignments = Assignment.objects.filter(
            course=c
        )

        c_total = c_assignments.count()

        if c_total == 0:
            c.progress = 0
            continue

        c_submissions = Submission.objects.filter(
            student=student,
            assignment__in=c_assignments,
            status__in=["submitted", "graded"],
        ).select_related("assignment")

        c_percent_total = 0.0

        for s in c_submissions:
            c_percent_total += float(
                getattr(s, "percentage", 0) or 0
            )

        c.progress = int(
            round(c_percent_total / c_total)
        )

    # =========================
    # COMPLETED ASSIGNMENTS
    # =========================
    completed_assignments = Submission.objects.filter(
        student=student,
        assignment__in=assignments,
        status__in=["submitted", "graded"]
    ).count()

    # =========================
    # RENDER TEMPLATE
    # =========================
    return render(
        request,
        "dashboard/student_dashboard.html",
        {
            "student": student,
            "courses": courses,
            "assignments": assignments,
            "topics": topics,

            "total_courses": courses.count(),
            "total_assignments": total_assignments,
            "completed_assignments": completed_assignments,
            "total_topics": topics.count(),

            "certificates": certificates,
            "progress_percent": progress_percent,
        }
    )
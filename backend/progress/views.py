from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from assignments.models import Assignment, Submission
from coding_tasks.models import CodingSubmission
from django.db.models import Sum
from courses.models import Course
from accounts.models import User
from notifications.utils import send_notification
from .models import Progress


def _compute_course_progress(student, course):
    """
    Compute progress for a single (student, course) pair based on assignments
    submissions + coding submissions. This is used as a fallback when no
    Progress record exists (so existing behavior continues to work).
    """
    assignments = Assignment.objects.filter(course=course)
    total_assignments = assignments.count()

    completed_assignments = Submission.objects.filter(
        student=student,
        assignment__in=assignments,
        status__in=["submitted", "graded"],
    ).count()

    coding = CodingSubmission.objects.filter(student=student, task__course=course)
    passed = coding.filter(status="Passed").count()
    total_coding = coding.count()

    total_items = total_assignments + total_coding
    completed_items = completed_assignments + passed

    progress_percent = int((completed_items / total_items) * 100) if total_items > 0 else 0

    # Score should reflect both assignment scores (MCQ auto-graded + PDF/GForm trainer-graded)
    # and coding task scores.
    assignment_score = (
        Submission.objects.filter(
            student=student,
            assignment__in=assignments,
            status__in=["submitted", "graded"],
        ).aggregate(total=Sum("score"))["total"]
        or 0
    )

    coding_score = coding.aggregate(total=Sum("score"))["total"] or 0
    score = int(assignment_score) + int(coding_score)

    return {
        "attendance": progress_percent,
        "score": score,
        "completed": progress_percent >= 70,
        "certificate_issued": progress_percent >= 90,
    }


# =========================
# STUDENT PROGRESS
# =========================

@login_required
def student_progress(request):

    if request.user.role != 'student':
        return redirect('login')

    student = request.user

    # Courses the student is enrolled in
    courses = Course.objects.filter(students=student)

    # Prefer saved Progress records (editable via Django admin).
    # If a record doesn't exist, fall back to computed values so existing
    # functionality still works.
    saved_progress = {
        p.course_id: p
        for p in Progress.objects.filter(student=student, course__in=courses).select_related("course")
    }

    progress_list = []
    for course in courses:
        p = saved_progress.get(course.id)
        if p is None:
            computed = _compute_course_progress(student, course)
            p = Progress(
                student=student,
                course=course,
                attendance=computed["attendance"],
                score=computed["score"],
                completed=computed["completed"],
                certificate_issued=computed["certificate_issued"],
            )
        progress_list.append(p)

    return render(request, 'progress/student_progress.html', {
        'progress': progress_list,
    })
# =========================
# TRAINER PROGRESS
# =========================

@login_required
def trainer_progress(request):

    if request.user.role != 'trainer':
        return redirect('login')

    # Students assigned to this trainer
    students = User.objects.filter(trainer=request.user, role="student")

    progress_rows = []

    # Fetch saved Progress records once for efficiency
    saved_qs = (
        Progress.objects.filter(student__in=students, course__trainer=request.user)
        .select_related("student", "course")
    )
    saved_map = {(p.student_id, p.course_id): p for p in saved_qs}

    for student in students:
        student_courses = Course.objects.filter(students=student, trainer=request.user)
        for course in student_courses:
            p = saved_map.get((student.id, course.id))
            if p is None:
                computed = _compute_course_progress(student, course)
                p = Progress(
                    student=student,
                    course=course,
                    attendance=computed["attendance"],
                    score=computed["score"],
                    completed=computed["completed"],
                    certificate_issued=computed["certificate_issued"],
                )
            progress_rows.append(p)

    return render(request, 'progress/trainer_progress.html', {'progress': progress_rows})


# =========================
# ADMIN PROGRESS
# =========================

@login_required
def admin_progress(request):

    if request.user.role != 'admin':
        return redirect('login')

    # Admin view: show progress for all enrolled (student, course) pairs.
    # If a saved Progress record doesn't exist, compute it on the fly so the page
    # doesn't look "empty".
    courses = Course.objects.all().prefetch_related("students")
    students = User.objects.filter(role="student")

    saved_qs = Progress.objects.select_related("student", "course").all()
    saved_map = {(p.student_id, p.course_id): p for p in saved_qs}

    progress_rows = []
    # Build rows only for enrolled students (avoid showing random combinations)
    for course in courses:
        for student in course.students.filter(role="student"):
            p = saved_map.get((student.id, course.id))
            if p is None:
                computed = _compute_course_progress(student, course)
                p = Progress(
                    student=student,
                    course=course,
                    attendance=computed["attendance"],
                    score=computed["score"],
                    completed=computed["completed"],
                    certificate_issued=computed["certificate_issued"],
                )
            progress_rows.append(p)

    return render(request, 'progress/admin_progress.html', {'progress': progress_rows})

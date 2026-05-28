from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Count,
    Sum,
    F,
    FloatField,
    ExpressionWrapper,
    Case,
    When,
    IntegerField,
)

from assignments.models import Assignment, Submission
from coding_tasks.models import CodingSubmission, CodingTask
from attendance.models import Attendance
from courses.models import Course
from accounts.models import User
from notifications.utils import send_notification
from .models import Progress


# =========================================================
# ATTENDANCE PERCENT MAP
# =========================================================
def _get_attendance_percent_map(user_ids):

    if not user_ids:
        return {}

    rows = (
        Attendance.objects.filter(user_id__in=user_ids)
        .exclude(status="Pending")
        .values("user_id")
        .annotate(
            total=Count("id"),
            present=Sum(
                Case(
                    When(status="Present", then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
        )
    )

    result = {uid: 0 for uid in user_ids}

    for row in rows:

        total = row["total"] or 0
        present = row["present"] or 0

        result[row["user_id"]] = (
            int(round((present * 100.0) / total))
            if total > 0
            else 0
        )

    return result


# =========================================================
# ASSIGNMENT COUNT MAP
# =========================================================
def _get_course_assignment_count_map(course_ids):

    if not course_ids:
        return {}

    rows = (
        Assignment.objects.filter(course_id__in=course_ids)
        .values("course_id")
        .annotate(cnt=Count("id"))
    )

    return {
        row["course_id"]: (row["cnt"] or 0)
        for row in rows
    }


# =========================================================
# SUBMISSION PERCENT MAP
# =========================================================
def _get_submission_sum_percent_map(student_ids, course_ids):

    if not student_ids or not course_ids:
        return {}

    percent_expr = ExpressionWrapper(
        100.0 * F("score") / F("assignment__total_marks"),
        output_field=FloatField(),
    )

    rows = (
        Submission.objects.filter(
            student_id__in=student_ids,
            assignment__course_id__in=course_ids,
            status__in=["submitted", "graded"],
            assignment__total_marks__gt=0,
        )
        .annotate(percent=percent_expr)
        .values("student_id", "assignment__course_id")
        .annotate(sum_percent=Sum("percent"))
    )

    result = {}

    for row in rows:
        result[
            (
                row["student_id"],
                row["assignment__course_id"]
            )
        ] = float(row["sum_percent"] or 0.0)

    return result


# =========================================================
# ATTACH EXTRA METRICS
# =========================================================
def _attach_progress_metrics(progress_rows):

    if not progress_rows:
        return

    student_ids = {
        p.student_id
        for p in progress_rows
    }

    course_ids = {
        p.course_id
        for p in progress_rows
    }

    attendance_map = _get_attendance_percent_map(student_ids)

    assignment_count_map = _get_course_assignment_count_map(
        course_ids
    )

    sum_percent_map = _get_submission_sum_percent_map(
        student_ids,
        course_ids,
    )

    for p in progress_rows:

        p.attendance_percent = attendance_map.get(
            p.student_id,
            0
        )

        total_assignments = assignment_count_map.get(
            p.course_id,
            0
        )

        sum_percent = sum_percent_map.get(
            (p.student_id, p.course_id),
            0.0
        )

        p.assignment_avg_score = (
            round((sum_percent / total_assignments), 1)
            if total_assignments > 0
            else 0
        )

        try:
            p.score = int(round(p.assignment_avg_score))
        except Exception:
            p.score = 0


# =========================================================
# COMPUTE COURSE PROGRESS
# =========================================================
def _compute_course_progress(student, course):

    # -----------------------------
    # ASSIGNMENTS
    # -----------------------------
    assignments = Assignment.objects.filter(
        course=course
    )

    total_assignments = assignments.count()

    submissions = (
        Submission.objects.filter(
            student=student,
            assignment__in=assignments,
            status__in=["submitted", "graded"],
        )
        .select_related("assignment")
    )

    assignment_percent_total = 0.0

    for submission in submissions:

        assignment_percent_total += float(
            getattr(submission, "percentage", 0) or 0
        )

    # -----------------------------
    # CODING TASKS
    # -----------------------------
    coding_tasks = CodingTask.objects.filter(
        course=course
    )

    total_tasks = coding_tasks.count()

    coding_submissions = (
        CodingSubmission.objects.filter(
            student=student,
            task__in=coding_tasks
        )
        .select_related("task")
    )

    coding_percent_total = 0.0

    for coding in coding_submissions:

        marks = getattr(coding.task, "marks", 0) or 0

        if marks > 0:

            coding_percent_total += (
                (
                    float(coding.score or 0)
                    / float(marks)
                ) * 100.0
            )

    # -----------------------------
    # OVERALL PROGRESS
    # -----------------------------
    total_items = total_assignments + total_tasks

    progress_percent = (
        int(
            round(
                (
                    assignment_percent_total
                    + coding_percent_total
                ) / total_items
            )
        )
        if total_items > 0
        else 0
    )

    score = progress_percent

    return {
        "attendance": progress_percent,
        "score": score,
        "completed": progress_percent >= 70,
        "certificate_issued": progress_percent >= 90,
    }


# =========================================================
# STUDENT PROGRESS
# =========================================================
@login_required
def student_progress(request):

    if request.user.role != "student":
        return redirect("login")

    student = request.user

    courses = Course.objects.filter(
        students=student
    )

    saved_progress = {
        p.course_id: p
        for p in Progress.objects.filter(
            student=student,
            course__in=courses
        ).select_related("course")
    }

    progress_list = []

    for course in courses:

        progress = saved_progress.get(course.id)

        if progress is None:

            computed = _compute_course_progress(
                student,
                course
            )

            progress = Progress(
                student=student,
                course=course,
                attendance=computed["attendance"],
                score=computed["score"],
                completed=computed["completed"],
                certificate_issued=computed["certificate_issued"],
            )

        progress_list.append(progress)

    _attach_progress_metrics(progress_list)

    return render(
        request,
        "progress/student_progress.html",
        {
            "progress": progress_list,
        }
    )


# =========================================================
# TRAINER PROGRESS
# =========================================================
@login_required
def trainer_progress(request):

    if request.user.role != "trainer":
        return redirect("login")

    students = User.objects.filter(
        trainer=request.user,
        role="student"
    )

    progress_rows = []

    saved_qs = (
        Progress.objects.filter(
            student__in=students,
            course__trainer=request.user,
        )
        .select_related("student", "course")
    )

    saved_map = {
        (p.student_id, p.course_id): p
        for p in saved_qs
    }

    for student in students:

        student_courses = Course.objects.filter(
            students=student,
            trainer=request.user,
        )

        for course in student_courses:

            progress = saved_map.get(
                (student.id, course.id)
            )

            if progress is None:

                computed = _compute_course_progress(
                    student,
                    course
                )

                progress = Progress(
                    student=student,
                    course=course,
                    attendance=computed["attendance"],
                    score=computed["score"],
                    completed=computed["completed"],
                    certificate_issued=computed["certificate_issued"],
                )

            progress_rows.append(progress)

    _attach_progress_metrics(progress_rows)

    return render(
        request,
        "progress/trainer_progress.html",
        {
            "progress": progress_rows
        }
    )


# =========================================================
# ADMIN PROGRESS
# =========================================================
@login_required
def admin_progress(request):

    if request.user.role != "admin":
        return redirect("login")

    courses = Course.objects.all().prefetch_related(
        "students"
    )

    saved_qs = (
        Progress.objects.select_related(
            "student",
            "course"
        ).all()
    )

    saved_map = {
        (p.student_id, p.course_id): p
        for p in saved_qs
    }

    progress_rows = []

    for course in courses:

        students = course.students.filter(
            role="student"
        )

        for student in students:

            progress = saved_map.get(
                (student.id, course.id)
            )

            if progress is None:

                computed = _compute_course_progress(
                    student,
                    course
                )

                progress = Progress(
                    student=student,
                    course=course,
                    attendance=computed["attendance"],
                    score=computed["score"],
                    completed=computed["completed"],
                    certificate_issued=computed["certificate_issued"],
                )

            progress_rows.append(progress)

    _attach_progress_metrics(progress_rows)

    return render(
        request,
        "progress/admin_progress.html",
        {
            "progress": progress_rows
        }
    )
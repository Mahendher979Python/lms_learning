from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CodingTask, CodingSubmission
from courses.models import Course


# =========================================
# TRAINER CREATE TASK
# =========================================
@login_required
def create_task(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        difficulty = request.POST.get("difficulty")
        marks = request.POST.get("marks")
        expected_output = request.POST.get("expected_output")
        starter_code = request.POST.get("starter_code")
        course_id = request.POST.get("course")

        # VALIDATION
        if not title or not description or not marks:
            messages.error(request, "Please fill all required fields.")
            return redirect("coding_tasks:create_task")

        try:
            marks = int(marks)
        except ValueError:
            messages.error(request, "Marks must be a number.")
            return redirect("coding_tasks:create_task")

        course = Course.objects.get(id=course_id)

        CodingTask.objects.create(
            title=title,
            description=description,
            difficulty=difficulty,
            marks=marks,
            expected_output=expected_output,
            starter_code=starter_code,
            course=course,
            created_by=request.user
        )

        messages.success(request, "Coding task created successfully.")
        return redirect("coding_tasks:create_task")

    courses = Course.objects.all()

    return render(request, "coding_tasks/create_task.html", {
        "courses": courses
    })


# =========================================
# STUDENT AVAILABLE TASKS
# =========================================
@login_required
def available_tasks(request):

    tasks = CodingTask.objects.all().order_by("-created_at")

    return render(request, "coding_tasks/available_tasks.html", {
        "tasks": tasks
    })


# =========================================
# STUDENT SUBMIT TASK
# =========================================
@login_required
def submit_task(request, task_id):

    task = get_object_or_404(CodingTask, id=task_id)

    if request.method == "POST":

        submitted_code = request.POST.get("submitted_code", "")

        result = "Failed"
        score = 0

        # SIMPLE AUTO CHECK
        if task.expected_output.lower() in submitted_code.lower():
            result = "Passed"
            score = task.marks

        CodingSubmission.objects.create(
            task=task,
            student=request.user,
            submitted_code=submitted_code,
            output=task.expected_output,
            score=score,
            status=result
        )

        messages.success(request, "Code submitted successfully.")
        return redirect("coding_tasks:my_submissions")

    return render(request, "coding_tasks/submit_task.html", {
        "task": task
    })


# =========================================
# STUDENT SUBMISSIONS
# =========================================
@login_required
def my_submissions(request):

    submissions = CodingSubmission.objects.filter(
        student=request.user
    ).order_by("-submitted_at")

    return render(request, "coding_tasks/my_submissions.html", {
        "submissions": submissions
    })
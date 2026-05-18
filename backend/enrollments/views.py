from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollment
from courses.models import Course

@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)

    # prevent duplicate
    existing = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    if not existing:
        Enrollment.objects.create(
            student=request.user,
            course=course
        )

    return redirect('student_courses')

@login_required
def approve_enrollment(request, id):
    if request.user.role != 'admin':
        return redirect('login')

    enrollment = Enrollment.objects.get(id=id)
    enrollment.status = 'approved'
    enrollment.save()

    return redirect('admin_enrollments')

@login_required
def admin_enrollments(request):
    if request.user.role != 'admin':
        return redirect('login')

    enrollments = Enrollment.objects.all()

    return render(request, 'enrollments/admin_enrollments.html', {
        'enrollments': enrollments
    })

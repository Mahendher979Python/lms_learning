from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from notifications.utils import send_notification
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import Course, Topic, Payment
from certificates.models import Certificate
from .forms import CourseForm
from .utils import generate_upi_qr
from django.contrib.auth import get_user_model
from teams.models import Team
import hmac
import hashlib
from datetime import date
from django.http import JsonResponse, HttpResponse


from django.template.loader import get_template
from django.core.mail import EmailMessage


User = get_user_model()
# =====================================
# ADMIN - VIEW COURSES
# =====================================
@login_required
def admin_courses(request):
    if request.user.role != 'admin':
        return redirect('login')

    search_query = request.GET.get('q', '')

    courses = Course.objects.all().select_related('trainer').order_by('-updated_at')

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(trainer__username__icontains=search_query)
        )

    total_courses = courses.count()

    paginator = Paginator(courses, 5)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    return render(request, 'courses/admin_courses.html', {
        'courses': courses,
        'total_courses': total_courses,
        'search_query': search_query
    })

@login_required
def admin_payments(request):
    if request.user.role != "admin":
        return redirect("login")

    payments = Payment.objects.select_related(
        "student",
        "course"
    ).order_by("-paid_at")

    return render(request, "courses/admin_payments.html", {
        "payments": payments
    })


@login_required
def mark_payment_success(request, payment_id):
    if request.user.role != "admin":
        return redirect("login")

    payment = get_object_or_404(Payment, id=payment_id)

    if payment.payment_status != "success":
        payment.payment_status = "success"
        payment.save(update_fields=["payment_status"])

        payment.course.students.add(payment.student)

        send_notification(
            recipient=payment.student,
            sender=None,
            notif_type="payment",
            message=f"Payment marked successful for course '{payment.course.title}'",
            course_name=payment.course.title
        )

        if payment.course.trainer:
            send_notification(
                recipient=payment.course.trainer,
                sender=payment.student,
                notif_type="payment",
                message=f"{payment.student.username} enrolled in '{payment.course.title}'",
                course_name=payment.course.title
            )

    return redirect("admin_payments")


# =====================================
# ADMIN - CREATE COURSE
# =====================================

@login_required
def admin_create_course(request):

    if request.user.role != 'admin':
        return redirect('login')

    form = CourseForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        course = form.save(commit=False)

        # Free course auto price
        if course.course_type == 'free':
            course.price = 0

        trainer = form.cleaned_data.get('trainer')

        if not trainer:

            return render(
                request,
                'courses/course_form.html',
                {
                    'form': form,
                    'title': 'Create Course',
                    'error': 'Trainer is required'
                }
            )

        course.trainer = trainer

        course.save()
        # notify trainer
        send_notification(
            recipient=trainer,
            sender=request.user,
            notif_type='course',
            message=f"You have been assigned to course '{course.title}'",
            course_name=course.title
        )
        # many to many
        form.save_m2m()

        # selected students
        selected_students = form.cleaned_data.get('students')

        if selected_students:
            course.students.set(selected_students)

        # auto create team
        team = Team.objects.create(
            name=f"{course.title} Team",
            course=course,
            trainer=trainer
        )

        if selected_students:
            team.students.set(selected_students)

        # ===================================
        # SEND NOTIFICATIONS
        # ===================================

        # Trainer notification
        send_notification(
            recipient=trainer,
            sender=request.user,
            notif_type='enrollment',
            message=f"You have been assigned as trainer for {course.title}",
            course_name=course.title
        )

        # Student notifications
        if selected_students:

            for student in selected_students:

                send_notification(
                    recipient=student,
                    sender=request.user,
                    notif_type='enrollment',
                    message=f"You have been enrolled in {course.title}",
                    course_name=course.title
                )

        return redirect('admin_courses')

    return render(
        request,
        'courses/course_form.html',
        {
            'form': form,
            'title': 'Create Course'
        }
    )
# @login_required
# def admin_create_course(request):

#     if request.user.role != 'admin':
#         return redirect('login')

#     form = CourseForm(request.POST or None, request.FILES or None)

#     if form.is_valid():

#         # save course first
#         course = form.save(commit=False)

#         trainer = form.cleaned_data.get('trainer')

#         if not trainer:
#             return render(request, 'courses/course_form.html', {
#                 'form': form,
#                 'title': 'Create Course',
#                 'error': 'Trainer is required!'
#             })

#         # assign trainer
#         course.trainer = trainer
#         course.save()

#         # get students of this trainer
#         students = User.objects.filter(
#             role='student',
#             trainer=trainer
#         )

#         # assign students to course
#         course.students.set(students)

#         # create team automatically
#         team = Team.objects.create(
#             name=f"{course.title} Team",
#             course=course,
#             trainer=trainer
#         )

#         # assign students to team
#         team.students.set(students)

#         return redirect('admin_courses')

#     return render(request, 'courses/course_form.html', {
#         'form': form,
#         'title': 'Create Course'
#     }) 
# =====================================
# ADMIN - EDIT COURSE
# =====================================
@login_required
def edit_course(request, id):
    if request.user.role != 'admin':
        return redirect('login')

    course = get_object_or_404(Course, id=id)

    form = CourseForm(request.POST or None, request.FILES or None, instance=course)

    if form.is_valid():
        form.save()
        return redirect('admin_courses')

    return render(request, 'courses/course_form.html', {
        'form': form,
        'title': 'Edit Course'
    })


# =====================================
# ADMIN - DELETE COURSE
# =====================================
@login_required
def delete_course(request, id):
    if request.user.role != 'admin':
        return redirect('login')

    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        course.delete()
        return redirect('admin_courses')

    return render(request, "courses/confirm_delete.html", {
        "course": course
    })


# =====================================
# TRAINER - COURSES
# =====================================
@login_required
def trainer_courses(request):
    if request.user.role != "trainer":
        return redirect("login")

    search_query = request.GET.get('q', '')

    courses = Course.objects.filter(
        trainer=request.user
    ).prefetch_related('topics').order_by('-updated_at')

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    total_courses = courses.count()

    paginator = Paginator(courses, 5)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    return render(request, "courses/trainer_courses.html", {
        "courses": courses,
        "total_courses": total_courses,
        "search_query": search_query
    })

# =====================================
# ADMIN - CREATE TOPIC
# =====================================
@login_required
def admin_create_topic(request):
    if request.user.role != "admin":
        return redirect("login")

    courses = Course.objects.all()
    topics = Topic.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        course_id = request.POST.get("course")

        course = get_object_or_404(Course, id=course_id)

        Topic.objects.create(
            name=name,
            course=course,
            created_by=request.user,
            thumbnail=request.FILES.get("thumbnail"),
            video=request.FILES.get("video"),
            pdf=request.FILES.get("pdf"),
        )
        # notify students
        students = course.students.all()

        for student in students:
            send_notification(
                recipient=student,
                sender=request.user,
                notif_type='course',
                message=f"New topic '{name}' added in {course.title}",
                course_name=course.title
            )
        return redirect("admin_create_topic")

    return render(request, "courses/admin_create_topic.html", {
        "courses": courses,
        "topics": topics,
    })

# =====================================
# TRAINER - CREATE TOPIC
# =====================================
@login_required
def trainer_create_topic(request):
    if request.user.role != "trainer":
        return redirect("login")

    courses = Course.objects.filter(trainer=request.user)
    topics = Topic.objects.filter(course__trainer=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        course_id = request.POST.get("course")

        course = get_object_or_404(Course, id=course_id)

        Topic.objects.create(
            name=name,
            course=course,
            created_by=request.user,
            thumbnail=request.FILES.get("thumbnail"),
            video=request.FILES.get("video"),
            pdf=request.FILES.get("pdf"),
        )
        # notify students
        students = course.students.all()

        for student in students:
            send_notification(
                recipient=student,
                sender=request.user,
                notif_type='course',
                message=f"New topic '{name}' added in {course.title}",
                course_name=course.title
            )
        return redirect("trainer_create_topic")

    return render(request, "courses/trainer_create_topic.html", {
        "courses": courses,
        "topics": topics,
    })


# =====================================
# STUDENT - PURCHASED COURSES (FIXED)
# =====================================
@login_required
def student_courses(request):

    if request.user.role != "student":
        return redirect("login")

    search_query = request.GET.get('q', '')

    courses = Course.objects.all().prefetch_related('topics').order_by('-updated_at')

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    enrolled_courses = request.user.courses.all()

    total_courses = courses.count()

    return render(request, 'courses/student_courses.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'total_courses': total_courses,
        'search_query': search_query
    })
# =========================
# ASSIGNED COURSES PAGE
# =========================
@login_required
def assigned_courses(request):

    if request.user.role != "student":
        return redirect("login")

    search_query = request.GET.get('q', '')

    # ✅ GET USER COURSES
    courses = request.user.courses.all().prefetch_related('topics')

    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'courses/assigned_courses.html', {
        'courses': courses,
        'total_courses': courses.count(),
        'search_query': search_query
    })
# =====================================
# ASSIGNED COURSE DETAIL
# =====================================
@login_required
def assigned_course_detail(request, id):

    if request.user.role != "student":
        return redirect("login")

    course = get_object_or_404(
        Course,
        id=id
    )

    # only assigned students can open
    if course not in request.user.courses.all():

        return redirect(
            'assigned_course_details'
        )

    topics = Topic.objects.filter(
        course=course
    ).order_by('-id')

    return render(
        request,
        'courses/assigned_course_detail.html',
        {
            'course': course,
            'topics': topics
        }
    )
# =====================================
# COURSE DETAIL
# =====================================

@login_required
def course_detail(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    # =========================
    # ADMIN
    # =========================
    if request.user.role == "admin":

        return render(
            request,
            'courses/course_detail.html',
            {
                'course': course
            }
        )

    # =========================
    # TRAINER
    # =========================
    elif request.user.role == "trainer":

        if course.trainer != request.user:
            return redirect("trainer_courses")

        return render(
            request,
            'courses/course_detail.html',
            {
                'course': course
            }
        )

    # =========================
    # STUDENT
    # =========================
    elif request.user.role == "student":

        # assigned course access
        is_assigned = course in request.user.courses.all()

        # paid/enrolled access
        is_enrolled = course in request.user.enrolled_courses.all()

        # if neither assigned nor enrolled
        if not is_assigned and not is_enrolled:
            return redirect("assigned_courses")

        topics = Topic.objects.filter(
            course=course
        ).order_by('-id')

        return render(
            request,
            'courses/assigned_course_detail.html',
            {
                'course': course,
                'topics': topics,
                'is_enrolled': is_enrolled
            }
        )
    return redirect("login")


# =====================================
# EDIT TOPIC
# =====================================
@login_required
def edit_topic(request, id):
    topic = get_object_or_404(Topic, id=id)

    if request.user.role not in ["trainer", "admin"]:
        return redirect("login")

    if request.method == "POST":
        topic.name = request.POST.get("name")

        if request.FILES.get("thumbnail"):
            topic.thumbnail = request.FILES.get("thumbnail")

        if request.FILES.get("video"):
            topic.video = request.FILES.get("video")

        if request.FILES.get("pdf"):
            topic.pdf = request.FILES.get("pdf")

        topic.save()

        if request.user.role == "admin":
            return redirect("admin_create_topic")
        return redirect("trainer_courses")

    return render(request, "courses/edit_topic.html", {
        "topic": topic
    })


# =====================================
# DELETE TOPIC
# =====================================
@login_required
def delete_topic(request, id):
    topic = get_object_or_404(Topic, id=id)

    if request.user.role not in ["trainer", "admin"]:
        return redirect("login")

    if request.method == "POST":
        topic.delete()
        if request.user.role == "admin":
            return redirect("admin_create_topic")
        return redirect("trainer_courses")

    return render(request, "courses/confirm_delete.html", {
        "topic": topic
    })


# =====================================
# RAZORPAY PAYMENT
# =====================================


client = razorpay.Client(auth=(
    settings.RAZORPAY_KEY_ID,
    settings.RAZORPAY_KEY_SECRET
))

def create_payment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    amount = int(float(course.price) * 100)

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # store ONE record per order (important)
    Payment.objects.update_or_create(
        transaction_id=order['id'],
        defaults={
            "student": request.user,
            "course": course,
            "amount": course.price,
            "payment_status": "pending"
        }
    )

    return render(request, "courses/payment.html", {
        "order": order,
        "course": course,
        "key": settings.RAZORPAY_KEY_ID
    })
# =====================================
# PAYMENT SUCCESS
# =====================================

@csrf_exempt
def payment_success(request, course_id):
    if request.method != "POST":
        return JsonResponse({"status": "invalid"})

    try:
        data = json.loads(request.body)

        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        # 🔐 verify signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        payment = Payment.objects.get(
            transaction_id=data["razorpay_order_id"]
        )

        if payment.payment_status != "success":
            payment.payment_status = "success"
            payment.transaction_id = data["razorpay_payment_id"]
            payment.save()

            # enroll
            payment.course.students.add(payment.student)
            # notify student
            send_notification(
                recipient=payment.student,
                sender=None,
                notif_type='payment',
                message=f"Payment successful for course '{payment.course.title}'",
                course_name=payment.course.title
            )

            # notify trainer
            if payment.course.trainer:
                send_notification(
                    recipient=payment.course.trainer,
                    sender=payment.student,
                    notif_type='payment',
                    message=f"{payment.student.username} enrolled in '{payment.course.title}'",
                    course_name=payment.course.title
                )
        return JsonResponse({"status": "success"})

    except Exception as e:
        print("❌ VERIFY ERROR:", e)
        return JsonResponse({"status": "failed"})



@csrf_exempt
def razorpay_webhook(request):
    webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET

    body = request.body
    signature = request.headers.get('X-Razorpay-Signature')

    generated_signature = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(generated_signature, signature):
        return HttpResponse(status=400)

    payload = json.loads(body)

    if payload["event"] == "payment.captured":
        order_id = payload["payload"]["payment"]["entity"]["order_id"]
        payment_id = payload["payload"]["payment"]["entity"]["id"]

        try:
            payment = Payment.objects.get(transaction_id=order_id)

            if payment.payment_status != "success":
                payment.payment_status = "success"
                payment.transaction_id = payment_id
                payment.save()

                payment.course.students.add(payment.student)

        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)


# # =====================================
# # VIEW CERTIFICATE
# # =====================================
# @login_required
# def view_certificate(request, id):
#     certificate = get_object_or_404(Certificate, id=id)

#     return render(request, 'certificate.html', {
#         'certificate': certificate,
#         'student_name': certificate.user.username,
#         'course_title': certificate.course.title,
#         'completion_date': certificate.created_at,
#         'certificate_id': certificate.certificate_id,
#     })


# # =====================================
# # DOWNLOAD CERTIFICATE + EMAIL
# # =====================================
# @login_required
# def download_certificate(request, id):
#     certificate = get_object_or_404(Certificate, id=id)

#     template = get_template('certificate.html')

#     html = template.render({
#         'certificate': certificate,
#         'student_name': certificate.user.username,
#         'course_title': certificate.course.title,
#         'completion_date': certificate.created_at,
#         'certificate_id': certificate.certificate_id,
#     })

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

#     pisa.CreatePDF(html, dest=response)

#     # ✅ EMAIL
#     try:
#         email = EmailMessage(
#             subject="🎓 Certificate",
#             body="Your certificate is attached.",
#             from_email=settings.EMAIL_HOST_USER,
#             to=[certificate.user.email],
#         )
#         email.attach('certificate.pdf', response.content, 'application/pdf')
#         email.send()
#     except Exception as e:
#         print("Email error:", e)

#     return response


# # =====================================
# # STUDENT CERTIFICATES PAGE
# # =====================================
# @login_required
# def student_certificates(request):
#     certificates = Certificate.objects.filter(user=request.user)

#     return render(request, 'students/certificates.html', {
#         'certificates': certificates
#     })

def view_topic(request, id):
    topic = Topic.objects.get(id=id)
    return render(request, 'courses/view_topic.html', {'topic': topic})

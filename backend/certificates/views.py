from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.mail import EmailMessage

from .models import Certificate
from .forms import CertificateForm

from courses.models import Course
from progress.models import Progress
from accounts.models import User

# =========================
# NOTIFICATIONS
# =========================
from notifications.utils import send_notification


# =====================================
# TRAINER SEND CERTIFICATE TO ADMIN
# =====================================

@login_required
def send_certificate_request(request, course_id, student_id):

    if request.user.role != "trainer":
        return redirect("login")

    course = get_object_or_404(
        Course,
        id=course_id
    )

    # =========================
    # VALIDATION
    # =========================

    progress = Progress.objects.filter(
        student_id=student_id,
        course=course,
        completed=True
    ).first()

    if not progress:

        messages.error(
            request,
            "Student has not completed the course."
        )

        return redirect("trainer_progress")

    # =========================
    # CREATE CERTIFICATE
    # =========================

    certificate, created = Certificate.objects.get_or_create(

        student_id=student_id,
        course=course,

        defaults={

            'trainer': request.user,
            'completed': True,
        }
    )

    if request.method == "POST":

        form = CertificateForm(

            request.POST,
            request.FILES,
            instance=certificate
        )

        if form.is_valid():

            cert = form.save(commit=False)

            cert.status = "pending"

            cert.completed = True

            cert.trainer = request.user

            cert.save()

            # =====================================
            # ADMIN NOTIFICATIONS
            # =====================================

            admins = User.objects.filter(
                role='admin'
            )

            for admin in admins:

                send_notification(
                    recipient=admin,
                    sender=request.user,
                    notif_type='admin',
                    message=(
                        f"Certificate request submitted "
                        f"for {cert.student.username}"
                    ),
                    course_name=cert.course.title
                )

            # =====================================
            # STUDENT NOTIFICATION
            # =====================================

            send_notification(
                recipient=cert.student,
                sender=request.user,
                notif_type='course',
                message=(
                    f"Your certificate request "
                    f"was submitted for approval."
                ),
                course_name=cert.course.title
            )

            messages.success(
                request,
                "Certificate sent to admin for approval."
            )

            return redirect("trainer_dashboard")

    else:

        form = CertificateForm(
            instance=certificate
        )

    return render(

        request,

        'certificates/send_certificate.html',

        {

            'form': form,
            'certificate': certificate
        }
    )


# =====================================
# ADMIN CERTIFICATE REQUESTS
# =====================================

@login_required
def admin_certificate_requests(request):

    if request.user.role != "admin":
        return redirect("login")

    certificates = Certificate.objects.filter(
        status='pending'
    ).order_by('-created_at')

    return render(

        request,

        'certificates/admin_certificate_requests.html',

        {

            'certificates': certificates
        }
    )


# =====================================
# ADMIN APPROVE CERTIFICATE
# =====================================

@login_required
def approve_certificate(request, certificate_id):

    if request.user.role != "admin":
        return redirect("login")

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id
    )

    certificate.status = "approved"

    certificate.approved_by = request.user

    certificate.completed_at = timezone.now()

    certificate.save()

    # =====================================
    # STUDENT NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.student,
        sender=request.user,
        notif_type='course',
        message=(
            f"Your certificate for "
            f"{certificate.course.title} "
            f"has been approved."
        ),
        course_name=certificate.course.title
    )

    # =====================================
    # TRAINER NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.trainer,
        sender=request.user,
        notif_type='admin',
        message=(
            f"Certificate approved for "
            f"{certificate.student.username}."
        ),
        course_name=certificate.course.title
    )

    messages.success(
        request,
        "Certificate approved successfully."
    )

    return redirect(
        'admin_certificate_requests'
    )


# =====================================
# ADMIN REJECT CERTIFICATE
# =====================================

@login_required
def reject_certificate(request, certificate_id):

    if request.user.role != "admin":
        return redirect("login")

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id
    )

    certificate.status = "rejected"

    certificate.save()

    # =====================================
    # STUDENT NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.student,
        sender=request.user,
        notif_type='admin',
        message=(
            f"Your certificate for "
            f"{certificate.course.title} "
            f"was rejected."
        ),
        course_name=certificate.course.title
    )

    # =====================================
    # TRAINER NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.trainer,
        sender=request.user,
        notif_type='admin',
        message=(
            f"Certificate rejected for "
            f"{certificate.student.username}."
        ),
        course_name=certificate.course.title
    )

    messages.error(
        request,
        "Certificate rejected."
    )

    return redirect(
        'admin_certificate_requests'
    )


# =====================================
# VIEW CERTIFICATE
# =====================================

@login_required
def view_certificate(request, certificate_id):
    # NOTE: Previously this was restricted to `student=request.user`, which caused
    # "nothing happens" behavior for other roles (it results in a 404).
    certificate = get_object_or_404(Certificate, id=certificate_id)

    # Only approved certificates can be viewed as a certificate page
    if certificate.status != "approved":
        messages.error(request, "Certificate is not approved yet.")
        return redirect("my_certificates")

    role = getattr(request.user, "role", None)
    is_student_owner = certificate.student_id == request.user.id
    is_related_trainer = (
        certificate.trainer_id == request.user.id
        or getattr(certificate.course, "trainer_id", None) == request.user.id
    )

    if role == "admin" or is_student_owner or is_related_trainer:
        pass
    else:
        messages.error(request, "You are not allowed to view this certificate.")
        return redirect("my_certificates")

    return render(

        request,

        'certificates/certificate.html',

        {

            'certificate': certificate
        }
    )


# =====================================
# DOWNLOAD CERTIFICATE PDF
# =====================================

@login_required
def download_certificate(request, certificate_id):
    # NOTE: Previously this was restricted to `student=request.user`, which caused
    # 404s for admins/trainers even when a certificate existed.
    certificate = get_object_or_404(Certificate, id=certificate_id)

    if certificate.status != "approved":
        messages.error(request, "Certificate is not approved yet.")
        return redirect("my_certificates")

    role = getattr(request.user, "role", None)
    is_student_owner = certificate.student_id == request.user.id
    is_related_trainer = (
        certificate.trainer_id == request.user.id
        or getattr(certificate.course, "trainer_id", None) == request.user.id
    )

    if not (role == "admin" or is_student_owner or is_related_trainer):
        messages.error(request, "You are not allowed to download this certificate.")
        return redirect("my_certificates")

    # Render the same certificate design (HTML) and let the browser export PDF/PNG.
    # This gives an output that matches the on-screen certificate view.
    return render(
        request,
        "certificates/download_certificate.html",
        {"cert": certificate},
    )


# =====================================
# EMAIL CERTIFICATE
# =====================================

@login_required
def email_certificate(request, certificate_id):

    certificate = get_object_or_404(

        Certificate,

        id=certificate_id,

        student=request.user,

        status='approved'
    )

    subject = "Your Course Certificate"

    message = f"""

    Hello {certificate.student.username},

    Congratulations!

    Your certificate for the course
    "{certificate.course.title}"
    has been approved.

    Regards,
    LMS Team
    """

    email = EmailMessage(

        subject,

        message,

        to=[certificate.student.email]
    )

    email.send()

    # =====================================
    # EMAIL SENT NOTIFICATION
    # =====================================

    send_notification(
        recipient=certificate.student,
        sender=None,
        notif_type='message',
        message=(
            f"Certificate email sent for "
            f"{certificate.course.title}"
        ),
        course_name=certificate.course.title
    )

    messages.success(
        request,
        "Certificate emailed successfully."
    )

    return redirect(
        'my_certificates'
    )


# =====================================
# STUDENT CERTIFICATE LIST
# =====================================

@login_required
def my_certificates(request):

    certificates = Certificate.objects.filter(

        student=request.user,

        status='approved'
    ).order_by('-created_at')

    return render(

        request,

        'certificates/my_certificates.html',

        {

            'certificates': certificates
        }
    )

import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from courses.models import Course

User = get_user_model()


# =========================
# IMAGE SIZE VALIDATOR
# =========================
def validate_image_size(image):

    max_size = 5 * 1024 * 1024  # 5MB

    if image.size > max_size:
        raise ValidationError(
            "Image file too large (max 5MB)"
        )


# =========================
# CERTIFICATE MODEL
# =========================
class Certificate(models.Model):

    # =========================
    # STATUS CHOICES
    # =========================
    STATUS_CHOICES = [

        ('pending', 'Pending'),

        ('approved', 'Approved'),

        ('rejected', 'Rejected'),
    ]

    # =========================
    # STUDENT
    # =========================
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    # =========================
    # COURSE
    # =========================
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certificates'
    )

    # =========================
    # TRAINER
    # =========================
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trainer_certificates'
    )

    # =========================
    # APPROVED BY ADMIN
    # =========================
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_certificates'
    )

    # =========================
    # UNIQUE CERTIFICATE ID
    # =========================
    certificate_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    # =========================
    # STATUS
    # =========================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # =========================
    # COMPLETED
    # =========================
    completed = models.BooleanField(
        default=False
    )

    # =========================
    # DATES
    # =========================
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    issued_date = models.DateField(
        auto_now_add=True
    )

    # =========================
    # STUDENT PHOTO
    # =========================
    student_photo = models.ImageField(
        upload_to='certificate_students/',
        null=True,
        blank=True,
        validators=[validate_image_size],
        help_text="Student photo shown on certificate"
    )

    # =========================
    # DIRECTOR SIGNATURE
    # =========================
    director_signature = models.ImageField(
        upload_to='certificate_signatures/',
        null=True,
        blank=True,
        validators=[validate_image_size],
        help_text="Director signature shown on certificate"
    )

    # =========================
    # DIRECTOR NAME
    # =========================
    director_name = models.CharField(
        max_length=200,
        blank=True,
        default='Director'
    )

    # =========================
    # CERTIFICATE TITLE
    # =========================
    certificate_title = models.CharField(
        max_length=255,
        default='Certificate of Completion'
    )

    # =========================
    # DESCRIPTION
    # =========================
    description = models.TextField(
        blank=True,
        default='Successfully completed the course.'
    )

    # =========================
    # MODEL META
    # =========================
    class Meta:

        ordering = ['-created_at']

        unique_together = ['student', 'course']

    # =========================
    # STRING
    # =========================
    def __str__(self):

        return f"{self.student.username} - {self.course.title}"
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
import uuid

# =====================================
# Validators
# =====================================
def validate_1tb_file_size(file):
    # limit = 1 * 1024 * 1024 * 1024 * 1024  # 1 TB
    limit= 5 * 100 *1024* 1024 
    if file.size > limit:
        raise ValidationError("File size must be less than 1 TB.")


def validate_image_size(file):
    limit = 10 * 1024 * 1024  # 10 MB
    if file.size > limit:
        raise ValidationError("Image size must be less than 10 MB.")


# =====================================
# COURSE MODEL
# =====================================
class Course(models.Model):

    COURSE_TYPE = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    # ✅ NEW FIELD
    course_type = models.CharField(
        max_length=10,
        choices=COURSE_TYPE,
        default='free'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        validators=[validate_image_size]
    )

    demo_video = models.FileField(
        upload_to='demo_videos/',
        null=True,
        blank=True,
        validators=[validate_1tb_file_size]
    )

    video = models.FileField(
        upload_to='videos/',
        null=True,
        blank=True,
        validators=[validate_1tb_file_size]
    )

    material = models.FileField(
        upload_to='materials/',
        null=True,
        blank=True,
        validators=[validate_1tb_file_size]
    )

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'trainer'},
        related_name='taught_courses'
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_courses',
        blank=True,
        limit_choices_to={'role': 'student'}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # ✅ AUTO FREE PRICE
    def save(self, *args, **kwargs):

        if self.course_type == 'free':
            self.price = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        
# =====================================
# TOPIC MODEL
# =====================================
class Topic(models.Model):
    name = models.CharField(max_length=200)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='topics'
    )

    thumbnail = models.ImageField(
        upload_to='topics/thumbnails/',
        null=True,
        blank=True,
        validators=[validate_image_size]
    )

    video = models.FileField(
        upload_to='topics/videos/',
        null=True,
        blank=True,
        validators=[validate_1tb_file_size]
    )

    pdf = models.FileField(
        upload_to='topics/pdfs/',
        null=True,
        blank=True,
        validators=[validate_1tb_file_size]
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_topics',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =====================================
# PAYMENT MODEL
# =====================================
class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        limit_choices_to={'role': 'student'}
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    transaction_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"


# =====================================
# ENROLLMENT HELPER
# =====================================
def enroll_student_after_payment(student, course):
    course.students.add(student)


# # =========================
# # CERTIFICATE
# # =========================
# class Certificate(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='certificates'
#     )

#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='certificates'
#     )

#     certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     created_at     = models.DateTimeField(auto_now_add=True)
#     completed_at   = models.DateTimeField(null=True, blank=True)

#     # ── student photo shown on certificate ──
#     student_photo = models.ImageField(
#         upload_to='certificate_director/',
#         null=True, blank=True,
#         validators=[validate_image_size],
#         help_text="Director/Principal photo shown on certificate"
#     )

#     # ── Director signature shown on certificate ──
#     director_signature = models.ImageField(
#         upload_to='certificate_signatures/',
#         null=True, blank=True,
#         validators=[validate_image_size],
#         help_text="Director signature shown on certificate"
#     )

#     # ── Director name shown below signature on certificate ──
#     director_name = models.CharField(
#         max_length=200,
#         blank=True,
#         default='',
#         help_text="Director's name shown below signature on certificate"
#     )

#     def __str__(self):
#         return f"{self.user.username} - {self.course.title}"



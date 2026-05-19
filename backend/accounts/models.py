from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random


class User(AbstractUser):

    ROLE_CHOICES = (

        ('admin', 'Admin'),

        ('trainer', 'Trainer'),

        ('student', 'Student'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
    max_length=10,
    unique=True,
    null=True,
    blank=True
    )

    # =====================================
    # PROFILE FIELDS
    # =====================================

    gender = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    dob = models.DateField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )

    # =====================================
    # TRAINER FIELDS
    # =====================================

    specialization = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    experience = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    qualification = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    # =====================================
    # STUDENT - TRAINER RELATION
    # =====================================

    trainer = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    courses = models.ManyToManyField(
        'courses.Course',
        blank=True
    )

    def __str__(self):

        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"

    def is_expired(self):
        expiry_time = timezone.now() - timezone.timedelta(minutes=10)
        return self.created_at < expiry_time

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    unique=True
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
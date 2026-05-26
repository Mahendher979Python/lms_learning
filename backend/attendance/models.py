from django.db import models
from django.conf import settings
from django.utils import timezone


# =========================
# ATTENDANCE MODEL
# =========================

class Attendance(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    date = models.DateField(
        default=timezone.localdate
    )

    login_time = models.DateTimeField(
        null=True,
        blank=True
    )

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    total_hours = models.FloatField(
        default=0
    )

    # =========================
    # BREAK
    # =========================

    break_start = models.DateTimeField(
        null=True,
        blank=True
    )

    break_end = models.DateTimeField(
        null=True,
        blank=True
    )

    break_hours = models.FloatField(
        default=0
    )

    # =========================
    # LOCATION
    # =========================

    latitude = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    longitude = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    location_name = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # FACE IMAGE
    # =========================

    image = models.ImageField(
        upload_to='attendance_faces/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=(
            ("Present", "Present"),
            ("Absent", "Absent"),
            ("Pending", "Pending")
        ),
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "date"], name="unique_attendance_user_date")
        ]

    def save(self, *args, **kwargs):

        # Calculate total hours automatically
        if self.login_time and self.logout_time:

            diff = self.logout_time - self.login_time

            hours = diff.total_seconds() / 3600

            self.total_hours = round(
                hours - self.break_hours,
                2
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


# =========================
# BREAK MODEL
# =========================

class Break(models.Model):

    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='breaks'
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    total_break_hours = models.FloatField(
        default=0
    )

    def save(self, *args, **kwargs):

        if self.start_time and self.end_time:

            diff = self.end_time - self.start_time

            self.total_break_hours = round(
                diff.total_seconds() / 3600,
                2
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Break - {self.attendance.user.username}"


# =========================
# LIVE LOCATION TRACKING
# =========================

class LocationLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    latitude = models.CharField(
        max_length=100
    )

    longitude = models.CharField(
        max_length=100
    )

    tracked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} Location"


# =========================
# OPTIONAL:
# TRAINER - STUDENT ASSIGN
# =========================
"""
ADD THIS FIELD INSIDE YOUR CUSTOM USER MODEL
(accounts/models.py)

trainer = models.ForeignKey(
    'self',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assigned_students'
)
"""

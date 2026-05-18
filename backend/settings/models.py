from django.db import models
from django.conf import settings


class UserSettings(models.Model):

    LANGUAGE_CHOICES = [

        ('en', 'English'),

        ('te', 'Telugu'),

        ('hi', 'Hindi'),

    ]

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='user_settings'
    )

    language = models.CharField(

        max_length=10,

        choices=LANGUAGE_CHOICES,

        default='en'
    )

    dark_mode = models.BooleanField(
        default=False
    )

    email_notifications = models.BooleanField(
        default=True
    )

    push_notifications = models.BooleanField(
        default=True
    )

    fingerprint_login = models.BooleanField(
        default=False
    )

    two_factor_auth = models.BooleanField(
        default=False
    )

    autoplay_videos = models.BooleanField(
        default=True
    )

    offline_downloads = models.BooleanField(
        default=False
    )

    allow_chat = models.BooleanField(
        default=True
    )

    allow_discussions = models.BooleanField(
        default=True
    )

    live_class_reminders = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.user.username} Settings"
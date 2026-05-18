from django.db import models
from django.conf import settings


class Notification(models.Model):

    NOTIF_TYPES = (

        ('payment', 'Payment'),

        ('assignment_submitted',
         'Assignment Submitted'),

        ('assignment_review',
         'Assignment Review'),

        ('message', 'Message'),

        ('progress', 'Progress'),

        ('enrollment', 'Enrollment'),

        ('course', 'Course'),

        ('meeting', 'Meeting'),

        ('admin', 'Admin'),

    )

    # =====================================
    # RECEIVER
    # =====================================

    recipient = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='received_notifications'

    )

    # =====================================
    # SENDER
    # =====================================

    sender = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        null=True,

        blank=True,

        related_name='sent_notifications'

    )

    # =====================================
    # TYPE
    # =====================================

    type = models.CharField(

        max_length=50,

        choices=NOTIF_TYPES

    )

    # =====================================
    # TITLE
    # =====================================

    title = models.CharField(

        max_length=255,

        null=True,

        blank=True

    )

    # =====================================
    # MESSAGE
    # =====================================

    message = models.TextField()

    # =====================================
    # COURSE NAME
    # =====================================

    course_name = models.CharField(

        max_length=255,

        null=True,

        blank=True

    )

    # =====================================
    # PROGRESS %
    # =====================================

    progress = models.IntegerField(

        null=True,

        blank=True

    )

    # =====================================
    # READ STATUS
    # =====================================

    is_read = models.BooleanField(
        default=False
    )

    # =====================================
    # CREATED TIME
    # =====================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================
    # UPDATED TIME
    # =====================================

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================
    # MODEL SETTINGS
    # =====================================

    class Meta:

        ordering = ['-created_at']

        indexes = [

            models.Index(
                fields=['recipient']
            ),

            models.Index(
                fields=['is_read']
            ),

            models.Index(
                fields=['created_at']
            ),

            models.Index(
                fields=['type']
            ),

        ]

    # =====================================
    # STRING
    # =====================================

    def __str__(self):

        return f"{self.recipient.username} - {self.type}"

    # =====================================
    # MARK READ
    # =====================================

    def mark_as_read(self):

        if not self.is_read:

            self.is_read = True

            self.save(update_fields=['is_read'])

    # =====================================
    # SHORT MESSAGE
    # =====================================

    @property
    def short_message(self):

        if len(self.message) > 60:

            return self.message[:60] + "..."

        return self.message
from django.db import models
from django.conf import settings
from courses.models import Course


# =========================================
# TEAM
# =========================================

class Team(models.Model):

    name = models.CharField(
        max_length=100
    )

    course = models.ForeignKey(

        Course,

        on_delete=models.CASCADE,

        related_name='teams'
    )

    trainer = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='teams_as_trainer'
    )

    students = models.ManyToManyField(

        settings.AUTH_USER_MODEL,

        related_name='teams_as_student',

        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):

        return f"{self.name} - {self.course.title}"


# =========================================
# GROUP MESSAGE
# =========================================

class Message(models.Model):

    team = models.ForeignKey(

        Team,

        on_delete=models.CASCADE,

        related_name='messages'
    )

    sender = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE
    )

    content = models.TextField(
        blank=True
    )

    reply_to = models.ForeignKey(

        'self',

        null=True,

        blank=True,

        on_delete=models.SET_NULL
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    file = models.FileField(

        upload_to='group_chat_files/',

        blank=True,

        null=True
    )

    edited = models.BooleanField(
        default=False
    )

    class Meta:

        ordering = ['timestamp']

    def __str__(self):

        return f"{self.sender} - {self.team.name}"


# =========================================
# PRIVATE MESSAGE
# =========================================

class PrivateMessage(models.Model):

    sender = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='sent_pm'
    )

    receiver = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name='received_pm'
    )

    message = models.TextField(
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    file = models.FileField(

        upload_to='private_chat_files/',

        blank=True,

        null=True
    )

    is_read = models.BooleanField(
        default=False
    )

    class Meta:

        ordering = ['timestamp']

    def __str__(self):

        return f"{self.sender} -> {self.receiver}"


# =========================================
# PRIVATE CHAT REQUEST
# =========================================

class PrivateChatRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_private_chat_requests'
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_private_chat_requests'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    responded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ('requester', 'recipient')

    def __str__(self):
        return f"{self.requester} -> {self.recipient} ({self.status})"


# =========================================
# TEAM FILES
# =========================================

class File(models.Model):

    team = models.ForeignKey(

        Team,

        on_delete=models.CASCADE,

        related_name='files',

        null=True,

        blank=True
    )

    sender = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to='team_files/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.sender} uploaded file"


# =========================================
# REACTIONS
# =========================================

class Reaction(models.Model):

    message = models.ForeignKey(

        Message,

        on_delete=models.CASCADE,

        related_name="reactions"
    )

    user = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE
    )

    emoji = models.CharField(
        max_length=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = ['message', 'user']

    def __str__(self):

        return f"{self.user} reacted {self.emoji}"

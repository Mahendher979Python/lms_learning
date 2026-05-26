from django.db import models
from django.conf import settings

from courses.models import Course


class CourseBotConversation(models.Model):

    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name='doubt_bot_conversation'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"DoubtBot - {self.course.title}"


class CourseBotMessage(models.Model):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )

    conversation = models.ForeignKey(
        CourseBotConversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_bot_messages'
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    tokens_used = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.conversation.course.title} - {self.role} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class DoubtTicket(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('closed', 'Closed'),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='doubt_tickets'
    )

    title = models.CharField(
        max_length=255
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_doubt_tickets'
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_doubt_tickets'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='doubt_tickets',
        blank=True,
        through='DoubtTicketParticipant'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class DoubtTicketParticipant(models.Model):

    ticket = models.ForeignKey(
        DoubtTicket,
        on_delete=models.CASCADE,
        related_name='ticket_participants'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doubt_ticket_participations'
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('ticket', 'user')

    def __str__(self):
        return f"{self.ticket.id} - {self.user.username}"


class DoubtTicketInvite(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

    ticket = models.ForeignKey(
        DoubtTicket,
        on_delete=models.CASCADE,
        related_name='invites'
    )

    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_doubt_invites'
    )

    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_doubt_invites'
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
        unique_together = ('ticket', 'invited_user')

    def __str__(self):
        return f"{self.ticket.id} - {self.invited_user.username} - {self.status}"


class DoubtTicketMessage(models.Model):

    ticket = models.ForeignKey(
        DoubtTicket,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='doubt_ticket_messages'
    )

    sender_name = models.CharField(
        max_length=255,
        blank=True
    )

    is_ai = models.BooleanField(
        default=False
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.ticket.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


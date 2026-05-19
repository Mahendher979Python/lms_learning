from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversation(models.Model):
    """
    Model to store individual chat conversations for each user
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_conversations'
    )
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.title or self.title == "New Chat":
            first_message = self.messages.first()
            if first_message:
                self.title = first_message.content[:50] + "..." if len(first_message.content) > 50 else first_message.content
        super().save(*args, **kwargs)


class Message(models.Model):
    """
    Model to store individual messages within a conversation
    """
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f"{self.conversation.id} - {self.role} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ChatFile(models.Model):
    """
    Model to store files uploaded in chat conversations
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='files',
        null=True,
        blank=True
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='files',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_files'
    )
    file = models.FileField(upload_to='chat_files/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Chat File'
        verbose_name_plural = 'Chat Files'

    def __str__(self):
        return f"{self.filename} - {self.user.username}"


class ChatSettings(models.Model):
    """
    Model to store user preferences and settings for AI chat
    """
    THEME_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_settings'
    )
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='dark')
    model_preference = models.CharField(max_length=100, default='gemini-2.0-flash')
    temperature = models.FloatField(default=0.7)
    max_tokens = models.IntegerField(default=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Chat Settings'
        verbose_name_plural = 'Chat Settings'

    def __str__(self):
        return f"{self.user.username} - Chat Settings"


class TokenUsage(models.Model):
    """
    Model to track token usage for billing/analytics purposes
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='token_usage'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='token_usage'
    )
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    model_used = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Token Usage'
        verbose_name_plural = 'Token Usage'

    def __str__(self):
        return f"{self.user.username} - {self.total_tokens} tokens - {self.timestamp.strftime('%Y-%m-%d')}"

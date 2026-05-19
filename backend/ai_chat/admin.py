from django.contrib import admin
from .models import Conversation, Message, ChatFile, ChatSettings, TokenUsage


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username', 'user__email')
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'created_at', 'tokens_used')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'conversation__title')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


@admin.register(ChatFile)
class ChatFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'user', 'file_type', 'file_size', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('filename', 'user__username')
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('uploaded_at',)


@admin.register(ChatSettings)
class ChatSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'model_preference', 'temperature', 'max_tokens', 'updated_at')
    list_filter = ('theme', 'model_preference')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TokenUsage)
class TokenUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_tokens', 'model_used', 'timestamp')
    list_filter = ('model_used', 'timestamp')
    search_fields = ('user__username', 'model_used')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

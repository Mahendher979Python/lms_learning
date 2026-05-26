from django.contrib import admin
from .models import Team, Message, PrivateMessage, PrivateChatRequest


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'trainer')
    search_fields = ('name',)
    list_filter = ('course', 'trainer')
    filter_horizontal = ('students',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'team', 'timestamp')
    search_fields = ('content',)
    list_filter = ('team', 'sender')


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp')
    search_fields = ('message',)
    list_filter = ('sender', 'receiver')


@admin.register(PrivateChatRequest)
class PrivateChatRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'recipient', 'status', 'created_at')
    search_fields = ('requester__username', 'recipient__username')
    list_filter = ('status',)

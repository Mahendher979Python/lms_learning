from django.contrib import admin

from .models import (
    CourseBotConversation,
    CourseBotMessage,
    DoubtTicket,
    DoubtTicketMessage,
    DoubtTicketInvite,
    DoubtTicketParticipant,
)


@admin.register(CourseBotConversation)
class CourseBotConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'updated_at')
    search_fields = ('course__title',)


@admin.register(CourseBotMessage)
class CourseBotMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'role', 'created_at')
    search_fields = ('conversation__course__title', 'content')
    list_filter = ('role',)


@admin.register(DoubtTicket)
class DoubtTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'status', 'created_by', 'assigned_to', 'updated_at')
    search_fields = ('title', 'course__title', 'created_by__username', 'assigned_to__username')
    list_filter = ('status',)


@admin.register(DoubtTicketMessage)
class DoubtTicketMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'is_ai', 'created_at')
    search_fields = ('ticket__title', 'content', 'sender__username', 'sender_name')
    list_filter = ('is_ai',)


@admin.register(DoubtTicketInvite)
class DoubtTicketInviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'invited_by', 'invited_user', 'status', 'created_at')
    search_fields = ('ticket__title', 'invited_by__username', 'invited_user__username')
    list_filter = ('status',)


@admin.register(DoubtTicketParticipant)
class DoubtTicketParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'user', 'joined_at')
    search_fields = ('ticket__title', 'user__username')


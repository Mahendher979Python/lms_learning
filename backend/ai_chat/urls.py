from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('ask/', views.ask_ai, name='ask_ai'),
    path('conversations/', views.get_conversations, name='get_conversations'),
    path('conversations/create/', views.create_conversation, name='create_conversation'),
    path('conversations/<int:conversation_id>/', views.get_conversation_messages, name='get_conversation_messages'),
    path('conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('conversations/<int:conversation_id>/title/', views.update_conversation_title, name='update_conversation_title'),
    path('settings/', views.get_chat_settings, name='get_chat_settings'),
    path('settings/update/', views.update_chat_settings, name='update_chat_settings'),
]

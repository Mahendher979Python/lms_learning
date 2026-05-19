from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
import json
import logging

from .models import Conversation, Message, ChatFile, ChatSettings, TokenUsage

import google.generativeai as genai

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def chat_page(request):
    """
    Render the main chat page
    """
    return render(request, "ai_chat/chat.html")


@login_required
def get_conversations(request):
    """
    Get all conversations for the current user
    """
    conversations = Conversation.objects.filter(user=request.user, is_active=True)
    data = [
        {
            "id": conv.id,
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat()
        }
        for conv in conversations
    ]
    return JsonResponse({"conversations": data})


@login_required
def create_conversation(request):
    """
    Create a new conversation
    """
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "New Chat")
        
        conversation = Conversation.objects.create(
            user=request.user,
            title=title
        )
        
        return JsonResponse({
            "id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat()
        })
    
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def get_conversation_messages(request, conversation_id):
    """
    Get all messages for a specific conversation
    """
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id, 
        user=request.user
    )
    
    messages = Message.objects.filter(conversation=conversation)
    data = [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
            "tokens_used": msg.tokens_used
        }
        for msg in messages
    ]
    
    return JsonResponse({
        "conversation_id": conversation.id,
        "title": conversation.title,
        "messages": data
    })


@login_required
def delete_conversation(request, conversation_id):
    """
    Delete a conversation
    """
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id, 
        user=request.user
    )
    conversation.delete()
    return JsonResponse({"success": True})


@login_required
def update_conversation_title(request, conversation_id):
    """
    Update conversation title
    """
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title")
        
        conversation = get_object_or_404(
            Conversation, 
            id=conversation_id, 
            user=request.user
        )
        conversation.title = title
        conversation.save()
        
        return JsonResponse({"success": True, "title": conversation.title})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
@login_required
def ask_ai(request):
    """
    Send a message to AI and get response
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")
            conversation_id = data.get("conversation_id")

            if not message:
                return JsonResponse({"error": "Message is required"}, status=400)

            if conversation_id:
                conversation = get_object_or_404(
                    Conversation, 
                    id=conversation_id, 
                    user=request.user
                )
            else:
                conversation = Conversation.objects.create(
                    user=request.user,
                    title=message[:50] + "..." if len(message) > 50 else message
                )

            user_message = Message.objects.create(
                conversation=conversation,
                role="user",
                content=message
            )

            messages_history = Message.objects.filter(conversation=conversation).order_by('created_at')
            chat_history = []
            for msg in messages_history:
                chat_history.append({"role": msg.role, "parts": [msg.content]})

            response = model.generate_content(chat_history)
            ai_response = response.text if hasattr(response, 'text') else str(response)

            ai_message = Message.objects.create(
                conversation=conversation,
                role="assistant",
                content=ai_response
            )

            TokenUsage.objects.create(
                user=request.user,
                conversation=conversation,
                prompt_tokens=len(message.split()),
                completion_tokens=len(ai_response.split()),
                total_tokens=len(message.split()) + len(ai_response.split()),
                model_used="gemini-2.0-flash"
            )

            conversation.updated_at = timezone.now()
            conversation.save()

            return JsonResponse({
                "reply": ai_response,
                "conversation_id": conversation.id,
                "user_message_id": user_message.id,
                "ai_message_id": ai_message.id
            })

        except Exception as e:
            logger.error(f"AI Error: {str(e)}")
            return JsonResponse({"error": f"AI Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def get_chat_settings(request):
    """
    Get user chat settings
    """
    settings, created = ChatSettings.objects.get_or_create(user=request.user)
    return JsonResponse({
        "theme": settings.theme,
        "model_preference": settings.model_preference,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens
    })


@login_required
def update_chat_settings(request):
    """
    Update user chat settings
    """
    if request.method == "POST":
        data = json.loads(request.body)
        settings, created = ChatSettings.objects.get_or_create(user=request.user)
        
        if "theme" in data:
            settings.theme = data["theme"]
        if "model_preference" in data:
            settings.model_preference = data["model_preference"]
        if "temperature" in data:
            settings.temperature = data["temperature"]
        if "max_tokens" in data:
            settings.max_tokens = data["max_tokens"]
        
        settings.save()
        
        return JsonResponse({"success": True})
    
    return JsonResponse({"error": "Invalid request"}, status=400)

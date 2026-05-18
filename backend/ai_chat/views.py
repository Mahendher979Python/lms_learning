from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import google.generativeai as genai
import json

# Configure API
genai.configure(api_key=settings.GEMINI_API_KEY)

# ✅ NEW WORKING MODEL
model = genai.GenerativeModel("gemini-2.0-flash")


def chat_page(request):
    return render(request, "ai_chat/chat.html")


@csrf_exempt
def ask_ai(request):

    if request.method == "POST":

        data = json.loads(request.body)

        message = data.get("message")

        try:
            response = model.generate_content(message)

            return JsonResponse({
                "reply": response.text
            })

        except Exception as e:
            return JsonResponse({
                "reply": f"AI Error: {str(e)}"
            })

    return JsonResponse({
        "reply": "Invalid request"
    })
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/live/<room_code>/", consumers.LiveConsumer.as_asgi()),
]
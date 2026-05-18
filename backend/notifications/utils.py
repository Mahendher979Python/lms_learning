from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def send_notification(
    recipient,
    sender,
    notif_type,
    message,
    course_name=None,
    progress=None
):

    # Save notification in database
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        type=notif_type,
        message=message,
        course_name=course_name,
        progress=progress
    )

    # Realtime websocket push
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{recipient.id}",
        {
            "type": "send_notification",
            "data": {
                "id": notification.id,
                "notif_type": notif_type,
                "message": message,
                "course_name": course_name,
                "progress": progress,
                "created_at": str(notification.created_at),
                "sender": sender.username if sender else None,
            }
        }
    )

    return notification
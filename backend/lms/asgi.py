import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

import teams.routing
import courses.routing
import notifications.routing


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'lms.settings'
)

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({

    "http": django_asgi_app,

    "websocket": AuthMiddlewareStack(

        URLRouter(

            teams.routing.websocket_urlpatterns +

            courses.routing.websocket_urlpatterns +

            notifications.routing.websocket_urlpatterns
        )
    ),
})
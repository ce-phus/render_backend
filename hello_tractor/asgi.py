"""
ASGI config for hello_tractor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chats.routing import websocket_urlpatterns
from apps.chats.channels_middleware import JWTWebsocketMiddleware

settings_module = 'hello_tractor.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'hello_tractor.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTWebsocketMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    )
})

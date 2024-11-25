import os
import django
from django.core.asgi import get_asgi_application

settings_module = 'hello_tractor.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'hello_tractor.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chats.routing import websocket_urlpatterns
from apps.chats.channels_middleware import JWTWebsocketMiddleware


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

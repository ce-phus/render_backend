import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chats.routing import websocket_urlpatterns
from apps.chats.channels_middleware import JWTWebsocketMiddleware

# Setting the environment variable for the settings module
settings_module = 'hello_tractor.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'hello_tractor.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

# Initialize Django settings and ensure apps are loaded
django.setup()

# Define the ASGI application
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

from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from channels.db import database_sync_to_async
from django.db import close_old_connections

class JWTWebsocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        close_old_connections()

        query_string = scope.get("query_string", b"").decode("utf-8")
        query_parameters = dict(qp.split("=") for qp in query_string.split("&"))
        token  = query_parameters.get("token", None)

        if token is None:
            await send({
                "type": "websocket.close",
                "code": 4000
            })
            return
        
        authentication = JWTAuthentication()

        try:
            validated_token = authentication.get_validated_token(token)
            user = await database_sync_to_async(authentication.get_user)(validated_token)
            scope['user'] = user

            return await super().__call__(scope, receive, send)
        except AuthenticationFailed:
            await send({
                "type": "websocket.close",
                "code": 4002
            })
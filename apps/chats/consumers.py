import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_user = self.scope['user']
        if request_user.is_authenticated:
            chat_with_user = self.scope['url_route']['kwargs']['id']
            user_ids = [str(request_user.id), str(chat_with_user)]
            user_ids = sorted(user_ids)
            self.room_group_name = f'chat_{"-".join(user_ids)}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data =None, bytes_data=None):
        data = json.loads(text_data)
        user_id = str(self.scope['user'].id)

        if 'message' in data:
            message = data['message']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "user_id": user_id,
                    "content_type": "text"
                }
            )

        elif 'image' in data:
            image = data['image']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "image": image,
                    "user_id": user_id,
                    "content_type": "image"
                }
            )

    async def disconnect(self, code):
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def chat_message(self, event):
        user_id = event['user_id']
        content_type = event['content_type']
        
        if content_type == "text":
            message = event['message']
            await self.send(text_data=json.dumps({
                "content_type": content_type,
                "message": message,
                "userId": user_id,
            }))
        elif content_type == "image":
            image = event['image']
            await self.send(text_data=json.dumps({
                "content_type": content_type,
                "image": image,
                "userId": user_id,
            }))
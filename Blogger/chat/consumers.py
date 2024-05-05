import json
from channels.generic.websocket import AsyncWebsocketConsumer


class RoomChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "username": username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "username": username}))


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # current user's id
        self.current_user_id = self.scope["user"].id

        if self.scope['user'].is_authenticated:
            self.other_user_id = self.scope['url_route']['kwargs']['user_id']
            self.OneToOne_chat = f"chat__{self.current_user_id}_{self.other_user_id}"

            await self.channel_layer.group_add(self.OneToOne_chat, self.channel_name)
            await self.accept()

        else:
            self.close()
            
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.OneToOne_chat, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg = data['msg']
        uname = data['uname']

        await self.channel_layer.group_send(
            self.OneToOne_chat, {'type': 'private_chat', 'msg': msg, 'uname': uname}
        )

    async def private_chat(self, event):
        msg = event['msg']
        uname = event['uname']

        await self.send(text_data = json.dumps({'msg': msg, 'uname': uname}))






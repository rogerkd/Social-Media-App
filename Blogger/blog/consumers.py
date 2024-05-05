import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotifyConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope["user"].is_authenticated:      # If users r authenticated,
            self.user_group = "authenticated_users" # then create a common group to broadcast notifications

            await self.channel_layer.group_add(self.user_group, self.channel_name)
            await self.accept()
        else:
            self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group, self.channel_name)

    # receive notification from websocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        moto = data["moto"]
        notification = data["notification"]
        username = data["username"]

        # send notification to user_group
        await self.channel_layer.group_send(
            self.user_group, {'type': 'send_notification' ,'moto': moto, 'notification': notification, 'username': username}
        )

    # receive notification from user_group
    async def send_notification(self, event):
        moto = event['moto']
        notification = event['notification']
        username = event['username']

        # send notification back to websocket
        await self.send(text_data=json.dumps({'moto': moto,
                                            'notification': notification,
                                              'username': username}))
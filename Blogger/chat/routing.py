from django.urls import re_path
from . import consumers

chat_websocket_urlpatterns = [
    re_path(r"ws/roomChat/(?P<room_name>\w+)/$", consumers.RoomChatConsumer.as_asgi()),
    re_path(r"ws/privateChat/(?P<user_id>\w+)/$", consumers.PrivateChatConsumer.as_asgi()),
]
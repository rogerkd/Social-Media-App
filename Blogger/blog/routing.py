from django.urls import re_path
from blog import consumers

blog_websocket_urlpatterns = [
    re_path(r"ws/notify/$", consumers.NotifyConsumer.as_asgi()),
]
from django.contrib import admin
from .models import ChatRoom, Messages


# Combine Messages to ChatRoom
class MessagesInline(admin.StackedInline):
    model = Messages

# Extend ChatRoom
class ChatRoomAdmin(admin.ModelAdmin):
    model = ChatRoom
    inlines = [MessagesInline]

admin.site.register(ChatRoom, ChatRoomAdmin)

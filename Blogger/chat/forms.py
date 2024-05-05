from django import forms
from chat.models import ChatRoom, Messages

class ChatRoomForm(forms.ModelForm):

    class Meta:
        model = ChatRoom
        fields = ('room_name',)


class MessagesForm(forms.ModelForm):

    class Meta:
        model = Messages
        fields = ('room','content')
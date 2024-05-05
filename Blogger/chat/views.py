import json
import datetime
from django.contrib.auth.models import User
from blog.models import Profile
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View
from chat.models import ChatRoom, Messages, PrivateChat
from chat.forms import ChatRoomForm, MessagesForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import ListView
from  django.utils.timezone import make_aware

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Room Chatting
class RoomList(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat/home.html'
    context_object_name = 'room_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['username'] = json.dumps(str(self.request.user))
        return context
    

@login_required
def Save(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        if len(data) == 2:
            content = data.get("content")
            room = data.get("room_name")
            user = request.user

            chatroom = ChatRoom.objects.get(room_name=room)
            message = Messages(room=chatroom, user=user, content=content)
            message.save()

            return JsonResponse({'status': 'success'})
        
        elif len(data) == 1:
            room = data.get("room_name")
            if ChatRoom.objects.filter(room_name=room).exists():
                return JsonResponse({'status' : 'already_taken'})
            else:
                chatroom = ChatRoom(room_name=room)
                chatroom.save()
                return JsonResponse({'status' : 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
    
@login_required 
def join_room(request, room):
    if request.method == 'GET':
        # logged-in-user
        current_user = User.objects.get(id=request.user.id)

        # chatroom
        chatroom = ChatRoom.objects.get(room_name=room)

        if not chatroom.is_joined_by(current_user):
            chatroom.join(current_user)
            return JsonResponse({'status': 'joined'})
        else:
            return JsonResponse({'status': 'already_joined'})
    else:
        return JsonResponse({'status': 'failure'})
    
    
@login_required
def leave_room(request, room):
        if request.method == 'GET':
            # logged-in-user
            current_user = User.objects.get(id=request.user.id)

            # chatroom
            chatroom = ChatRoom.objects.get(room_name=room)
            chatroom.leave(current_user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure'})


@login_required
def Remove(request, room):
        try:
            chatroom = ChatRoom.objects.get(room_name=room)
            chatroom.delete()
            return redirect('room_list')
        except ChatRoom.DoesNotExist:
            return HttpResponse("Room not found", status=404)
        
    
class Room(LoginRequiredMixin, ListView):
    model = Messages
    template_name = 'chat/room.html'
    context_object_name = 'view_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Room
        context['room_name'] = self.kwargs['room_name']

        # logged-in-username
        context['user_name'] = json.dumps(str(self.request.user))

        # members in room
        chatroom = ChatRoom.objects.get(room_name=context['room_name'])
        context['members'] = chatroom.user_joined.all()
        context['members'] = json.dumps([str(i) for i in context['members']])
        
        # Room specific messages
        room_id = ChatRoom.objects.get(room_name=context['room_name']).id
        context['view_message'] = context['view_message'].filter(room = room_id)

        # logged-in-user specific messages
        context['user_message'] = context['view_message'].filter(user = self.request.user.id)

        # other-user messages
        context['other_message'] = context['view_message'].exclude(user = self.request.user.id)

        # retrieving unique date from 
        context['date'] = context['view_message'].values_list('timestamp__date', flat=True)
        context['date'] = list(set(context['date']))
        context['date'].sort()
        context['date'] = [date.isoformat() for date in context['date']]
        context['date'] = json.dumps(context['date'])
        
        # Converting into json format 
        context['view_message'] = serializers.serialize("json", context['view_message'])
        context['user_message'] = serializers.serialize("json", context['user_message'])
        context['other_message'] = serializers.serialize("json", context['other_message'])

        return context


# Private Chatting
class Private(LoginRequiredMixin, ListView):
    model = PrivateChat
    template_name = 'chat/private.html'
    context_object_name = 'private'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_id'] = self.kwargs['user_id']
        context['user_id'] = json.dumps(context['user_id'])
        context['current_user'] = json.dumps(str(self.request.user))

        return context
    


    

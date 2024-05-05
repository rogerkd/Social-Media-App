from django.db import models
from django.contrib.auth.models import User
from blog.models import Profile, Blog

# Room Chatting 
class ChatRoom(models.Model):
    room_name = models.CharField(max_length = 200)
    user_joined = models.ManyToManyField(
        User,
        symmetrical=False,
        related_name='joined_by',
        blank=True
    )

    def join(self, user):
        self.user_joined.add(user)

    def leave(self, user):
        self.user_joined.remove(user)

    def is_joined_by(self, user):
        flag = self.user_joined.filter(pk=user.pk).exists()
        return flag

    def __str__(self):
        return f"{self.room_name}"
    

class Messages(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField(blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user} {self.content} {self.timestamp}"
    
    class Meta:
        ordering = ["timestamp"]


# Private Chatting
class PrivateChat(models.Model):
    sender = models.ForeignKey(User, related_name='sent_msg', on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receive_msg', on_delete = models.CASCADE)
    content = models.TextField(null = True, blank = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.sender} {self.receiver} {self.content} {self.timestamp}"
    
    class Meta:
        ordering = ['timestamp']

from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name='Profile Picture')
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField(
        'self',
        related_name="followers",
        symmetrical=False,
        blank=True
    )

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()
    

    def __str__(self):
        return "{}".format(self.user.username)
    

    
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    blog_image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name='Blog Picture')
    date = models.DateTimeField(auto_now_add=True)
    i_likes = models.ManyToManyField(
        Profile,
        symmetrical=False,
        related_name='u_likes',
        blank=True
    )

    def liked_by(self, user_profile):
        self.i_likes.add(user_profile)
        self.save()

    def unliked_by(self, user_profile):
        self.i_likes.remove(user_profile)
        self.save()

    def is_liked_by(self, user_profile):
        flag = self.i_likes.filter(pk=user_profile.pk).exists()
        return flag
    

    def __str__(self):
        return "{} {} {}".format(self.author, self.title, self.date)
    
    class Meta:
        ordering = ["date"]



class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    commented_on = models.DateTimeField(auto_now_add=True)
    


class Notify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent', default=None)
    notification = models.TextField(blank=True, null=True)
    seen = models.BooleanField(default=False)
    notify_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["notify_date"]
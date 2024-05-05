from django import forms 
from .models import Blog, Profile


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('title', 'description', 'blog_image')

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('profile_image', 'bio', 'following')

  
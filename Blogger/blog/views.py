import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import BlogForm, ProfileForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from .models import Blog, Profile
from django import template
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
# from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from . tokens import generate_token 
# from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



class Home(ListView):
    model = Blog
    context_object_name = 'home'
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['feeds'] = context['home'].exclude(author=self.request.user.id)
        context['user_name'] = json.dumps(str(self.request.user))

        return context


class ViewBlog(LoginRequiredMixin, ListView):
    model = Blog
    context_object_name = 'view'
    template_name = 'blog/view_blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # # user specific data
        context['view'] = context['view'].filter(author=self.request.user.id)
        return context

   
class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    context_object_name = 'cb'
    template_name = 'blog/create_blog.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form =BlogForm(self.request.POST, self.request.FILES)
        form.instance.author = self.request.user
        form.save()
        return super(CreateBlog, self).form_valid(form)
    

class RemoveBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blog/remove_blog.html'
    context_object_name = 'view'
    
    def get_success_url(self):
        return reverse('view')


class CreateProfile(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    context_object_name = 'create_profile'
    template_name = 'blog/create_profile.html'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form = ProfileForm(self.request.POST)
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        form.save_m2m()
        
        return super(CreateProfile, self).form_valid(form)
        

class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('profile_image', 'bio', 'following')
    context_object_name = 'ep'
    template_name = "blog/create_profile.html"

    def get_success_url(self):
        return reverse('profile', kwargs={'pk':self.request.user.id})


@login_required
def like_blog(request, pk):
    if request.method == 'GET':
        # logged-in-user
        current_user_profile = Profile.objects.get(user_id = request.user.id)

        # other-user
        other_user = User.objects.get(id=pk)

        # other-user-blog
        other_user_blog = Blog.objects.get(author_id = pk)

        # if already liked the blog
        if other_user_blog.is_liked_by(current_user_profile):
            # then undo like
            other_user_blog.unliked_by(current_user_profile)
            return JsonResponse({'status': 'success', 'msg': str(request.user)+' likes your blog', 'uname': json.dumps(str(other_user)), 'likes_count': other_user_blog.i_likes.count()})

        # if already not liked the blog
        else:
            # then like
            other_user_blog.liked_by(current_user_profile)
            return JsonResponse({'status': 'success', 'msg': str(request.user)+' unlikes your blog', 'uname': json.dumps(str(other_user)), 'likes_count': other_user_blog.i_likes.count()})
    else:
        return JsonResponse({'status': 'failure'})


#---------------------------------------------------------------------------------------
@login_required
def profile(request, pk):

    try:
        profile = Profile.objects.get(user_id=pk)
    except Profile.DoesNotExist or ValueError:
        return redirect("create_profile")
    
    # logged-in user
    logged_in_user = request.user
    
    # list of all other user's profile
    other_profile_list = Profile.objects.exclude(user_id=logged_in_user.id)
    
    # profile of logged-in user
    user_profile = Profile.objects.get(user_id=logged_in_user.id)

    # list to store mutual profile's
    mutuals = []
    for other_profile in other_profile_list:
        if user_profile.is_following(other_profile) and other_profile.is_following(user_profile):
            mutuals.append(other_profile)
    
    context = {
        'profile':profile,
        'other_profile_list':other_profile_list,
        'mutuals':mutuals

    }

    return render(request, 'blog/profile.html', context)
        

@login_required
def follow_user(request, pk):

    # other user's profile
    other_user = User.objects.get(id=pk)
    other_profile = Profile.objects.get(user_id=other_user.id)

    # logged-in user's profile
    logged_in_user = request.user
    user_profile = Profile.objects.get(user_id=logged_in_user.id)

    if not user_profile.is_following(other_profile):
        user_profile.follow(other_profile)
    
    return redirect('profile', pk=request.user.id)


@login_required
def unfollow_user(request, pk):

    # other user's profile
    other_user = User.objects.get(id=pk)
    other_profile = Profile.objects.get(user_id=other_user.id)
    
    # logged-in user's profile
    logged_in_user = request.user
    user_profile = Profile.objects.get(user_id=logged_in_user.id)

    if user_profile.is_following(other_profile):
        user_profile.unfollow(other_profile)
    
    return redirect('profile', pk=request.user.id)
    

#----------------------------------------------------------------------------------------------------
def signup(request):
    if request.method=="POST":
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        c_pass = request.POST['c_pass']

        # Required Conditions

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already Registered.")
            return redirect('signup')

        if len(uname)>8:
            messages.error(request, "Username must be under 8 characters.")
            return redirect('signup')

        if pass1 != c_pass:
            messages.error(request, "Password didn't match")
            return redirect('signup')

        if not uname.isalnum():
            messages.error(request, "Username must be Alpha-Numerice")
            return redirect('signup')
        

        myuser = User.objects.create_user(username=uname,email=email,password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.email = email
        myuser.is_active = True
        myuser.save()
        # messages.success(request, "Your Account has been Successfully Created.")
        
        user = authenticate(username=uname, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('create_profile')
        else:
            return redirect('signup')
    
    return render(request, "blog/signup.html")



def signin(request):
    if request.method=='POST':
        uname = request.POST['uname']
        pass1 = request.POST['pass1']

        user = authenticate(username=uname, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')

        elif user is None:
            messages.error(request, "Invalid Inputs!!")
            return redirect('signin')

    return render(request, "blog/signin.html")


def signout(request):
    logout(request)
    return redirect('home')


def forgot_password(request):
    if request.method=='POST':
        uname = request.POST['uname']

        try:
            if User.objects.filter(username=uname).first():

                user = User.objects.get(username=uname)
                uid =  urlsafe_base64_encode(force_bytes(user.pk))
                uid = uid + '=='
                token = generate_token.make_token(user)
        
                return render(request, "blog/change_password_form.html", {'uid':uid, 'token':token})
            
            else:
                messages.error(request, 'Username not registered')
                return redirect("forgot_password")

        except Exception as e:
            print(e)
            
    return render(request, 'blog/forgot_password.html')



def change_password_form(request, uidb64, token):
    if request.method=='POST':

        pass1 = request.POST['pass1']
        c_pass = request.POST['c_pass']

        try:

            if pass1 != c_pass:
                messages.error(request, "Password didn't match")
                return render(request, 'blog/change_password_form.html', {'uid':uidb64, 'token':token})
            
            elif pass1 == c_pass:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                user.set_password(pass1)
                user.save()

                messages.success(request, "Password reset succesfully")
                return redirect('signin')

        except Exception as e:
            print(e)
    return render(request, 'blog/change_password_form.html', {'uid':uidb64, 'token':token})
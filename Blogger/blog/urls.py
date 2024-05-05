from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Home, CreateBlog, ViewBlog, RemoveBlog, CreateProfile, EditProfile

urlpatterns = [

    path('', Home.as_view(), name='home'),
    path('view_blog/', ViewBlog.as_view(), name='view'),
    path('create_blog/', CreateBlog.as_view(), name='create'),
    path('remove_blog/<int:pk>/', RemoveBlog.as_view(), name='remove_blog'),
    path('like_blog/<int:pk>/', views.like_blog, name='like'),

    path('edit_profile/<int:pk>/', EditProfile.as_view(), name = 'edit_profile'),
    path('create_profile/', CreateProfile.as_view(), name='create_profile'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    

    path('follow/<int:pk>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:pk>/', views.unfollow_user, name='unfollow_user'),

    path('signin/', views.signin, name = 'signin'),
    path('signup/', views.signup, name='signup'),
    path('signin/signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
]

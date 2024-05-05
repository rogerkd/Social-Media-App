from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Blog, Profile, Comment, Notify


admin.site.unregister(Group)

# combine comment to Blog
class CommentInline(admin.StackedInline):
    model = Comment

# extend Blog model
class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Blog, BlogAdmin)


# combine notify to user
class NotifyInline(admin.StackedInline):
    model = Notify
    fk_name = 'user'  # Use for relationship b/w Notify n User model

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        if obj is not None:   #if we are currently viewing an existing object
            formset.form.base_fields['sender'].queryset = formset.form.base_fields['sender'].queryset.exclude(id=obj.id)

        return formset


# Combine profile to user
class ProfileInline(admin.StackedInline):
    model = Profile
    

# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['first_name','last_name','email']
    inlines = [ProfileInline, NotifyInline]

    
# Unregister Initial User
admin.site.unregister(User)

# Register user and profile
admin.site.register(User, UserAdmin)


    


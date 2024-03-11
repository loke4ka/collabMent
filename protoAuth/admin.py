from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Friendship, Post, Like, Repost, Comment

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['professional_field', 'education', 'current_job', 'experience', 'location', 'personal_qualities', 'certificates', 'resume', 'profile_photo' , 'education_date' , 'name_institution', 'desired_position' , 'type_of_work', 'operating_mode' , 'name_organization', 'position', 'experience_name', 'citizenship', 'city' ]
    extra = 0

class FriendshipInline(admin.TabularInline):
    model = Friendship
    fk_name = 'user'

class PostsInline(admin.TabularInline):
    model = Post
    fk_name = 'author'

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'chat_token', 'birthday', 'gender', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone_number'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    inlines = [ProfileInline, FriendshipInline, PostsInline]

class CommentInline(admin.TabularInline):
    model = Comment
    fk_name = 'post'

class LikeInline(admin.TabularInline):
    model = Like
    fk_name = 'post'

class RepostInline(admin.TabularInline):
    model = Repost
    fk_name = 'post'


class PostAdmin(admin.ModelAdmin):
    list_filter = ('author', 'created_at')
    
    inlines = [CommentInline, LikeInline, RepostInline]

admin.site.register(Post,PostAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

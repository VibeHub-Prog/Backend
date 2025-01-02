from django.contrib import admin
from .models import User, Post, Vibe, Bookmark, Community, Membership

# Register the User model
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'is_google_user', 'is_staff')
#     search_fields = ('username', 'email')
#     list_filter = ('is_google_user', 'is_staff', 'is_active')

# Register the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)

# Register the Vibe model
@admin.register(Vibe)
class VibeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    search_fields = ('user__username', 'post__content')

# Register the Bookmark model
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    search_fields = ('user__username', 'post__content')

# Register the Community model
@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'is_default')
    search_fields = ('name', 'description')
    list_filter = ('is_default',)

# Register the Membership model
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'community')
    search_fields = ('user__username', 'community__name')

from django.contrib import admin
from .models import User, Post

# Register the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at',)




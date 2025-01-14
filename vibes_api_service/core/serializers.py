from rest_framework import serializers, viewsets
from .models import Post, Like, Comment, Share

class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    total_shares = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'image', 'video', 'created_at', 'updated_at', 'total_likes', 'total_comments', 'total_shares']




class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()  # For nested replies

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'parent', 'replies', 'created_at', 'updated_at']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ['id', 'user', 'post', 'created_at']
from rest_framework import serializers, viewsets
from .models import Post, Like, Comment, Share

from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)
    total_comments = serializers.IntegerField(read_only=True)
    total_shares = serializers.IntegerField(read_only=True)
    author = serializers.CharField()  # Accept and return the author's username as a string

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'image', 'video', 
            'created_at', 'updated_at', 'total_likes', 
            'total_comments', 'total_shares'
        ]

    def create(self, validated_data):
        # Get the username from the validated data
        username = validated_data.pop('author')
        # Fetch the User instance with the given username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"author": "User with this username does not exist."})
        # Create a Post instance
        return Post.objects.create(author=user, **validated_data)

    def update(self, instance, validated_data):
        # Allow updates to the `author` if provided
        if 'author' in validated_data:
            username = validated_data.pop('author')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError({"author": "User with this username does not exist."})
            instance.author = user
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        # Customize the representation to show `author` as a string (username)
        representation = super().to_representation(instance)
        representation['author'] = instance.author.username  # Return the username as a string
        return representation




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
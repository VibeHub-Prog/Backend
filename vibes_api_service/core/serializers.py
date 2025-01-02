from rest_framework import serializers
from .models import Post, Community, Vibe, Bookmark

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


from rest_framework import serializers, viewsets

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class VibeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vibe
        fields = ('id', 'user', 'post')


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'post')
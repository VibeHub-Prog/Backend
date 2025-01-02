from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView
from .models import Post, Community, Vibe, Bookmark
from .serializers import PostsSerializer, CommunitySerializer,PostSerializer, VibeSerializer, BookmarkSerializer

from rest_framework import serializers, viewsets

class PostsListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

class VibeViewSet(viewsets.ModelViewSet):
    queryset = Vibe.objects.all()
    serializer_class = VibeSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
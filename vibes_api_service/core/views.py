from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Like, Comment, Share
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, ShareSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        Like.objects.get_or_create(user=request.user, post=post)
        return Response({'message': 'Post liked successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Post unliked successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def share(self, request, pk=None):
        post = self.get_object()
        Share.objects.get_or_create(user=request.user, post=post)
        return Response({'message': 'Post shared successfully.'})

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent')
        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(pk=parent_id)
        serializer.save(user=self.request.user, parent=parent_comment)


class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ShareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

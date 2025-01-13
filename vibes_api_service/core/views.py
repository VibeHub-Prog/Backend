from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Like, Comment, Share
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, ShareSerializer
from utils.email import EmailManager  # Assuming the EmailManager handles email notifications

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            EmailManager.send_notification_to_user(
                recipient_email=post.owner.email,
                subject="Your post has been liked",
                message=f"{request.user.username} liked your post.",
                username=request.user.username
            )
        return Response({'message': 'Post liked successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Post unliked successfully.'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def share(self, request, pk=None):
        post = self.get_object()
        share, created = Share.objects.get_or_create(user=request.user, post=post)
        if created:
            EmailManager.send_notification_to_user(
                recipient_email=post.owner.email,
                subject="Your post has been shared",
                message=f"{request.user.username} shared your post.",
                username=request.user.username
            )
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
        comment = serializer.save(user=self.request.user, parent=parent_comment)
        EmailManager.send_notification_to_user(
            recipient_email=comment.post.owner.email,
            subject="New comment on your post",
            message=f"{self.request.user.username} commented on your post.",
            username=self.request.user.username
        )
        if parent_comment:
            EmailManager.send_notification_to_user(
                recipient_email=parent_comment.user.email,
                subject="Someone replied to your comment",
                message=f"{self.request.user.username} replied to your comment.",
                username=self.request.user.username
            )

class LikeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ShareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

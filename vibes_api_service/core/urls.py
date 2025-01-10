from django.urls import path, include
from .views import PostsListCreateView, PostDetailView, PostDeleteView

from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, CommunityViewSet, MembershipViewSet, PostViewSet, VibeViewSet, BookmarkViewSet



router = DefaultRouter()
# router.register('messages', MessageViewSet, basename='messages')


router.register('posts', PostViewSet, basename='posts')
# router.register('vibes', VibeViewSet, basename='vibes')
# router.register('bookmarks', BookmarkViewSet, basename='bookmarks')

urlpatterns = [
    path('posts/', PostsListCreateView.as_view(), name='posts-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('', include(router.urls)),
]

from django.urls import path
from .views import PostsListCreateView, PostDetailView, PostDeleteView

urlpatterns = [
    path('posts/', PostsListCreateView.as_view(), name='posts-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]

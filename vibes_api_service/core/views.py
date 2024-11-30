from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView
from .models import Posts
from .serializers import PostsSerializer

class PostsListCreateView(ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class PostDeleteView(DestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
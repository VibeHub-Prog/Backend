from django.urls import path
from .views import ChatListView, MessageListView

urlpatterns = [
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:chat_id>/messages/', MessageListView.as_view(), name='message-list'),
]




# from .views import ChatRoomViewSet, MessageViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'chat', ChatRoomViewSet, basename='chatroom')
# router.register(r'messages', MessageViewSet, basename='message')

# urlpatterns = router.urls

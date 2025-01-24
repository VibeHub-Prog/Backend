from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from django.db.models import Q


class ChatListView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        participants = self.request.data.get('participants', [])
        if not isinstance(participants, list):
            raise serializers.ValidationError({'error': 'Participants must be a list of user IDs.'})
        if len(participants) != 2:
            raise serializers.ValidationError({'error': 'A chat must have exactly two participants.'})
        # if self.request.user.id not in participants:
        #     raise serializers.ValidationError({'error': 'You can only create chats that include yourself as a participant.'})
        participants = sorted(participants)
        existing_chat = Chat.objects.filter(
            Q(participants=participants[0]) & Q(participants=participants[1]) |
            Q(participants=participants[1]) & Q(participants=participants[0])
        ).distinct()
        if existing_chat.exists():
            raise serializers.ValidationError({'error': 'A chat between these participants already exists.'})
        serializer.save()



class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(chat__id=self.kwargs['chat_id']).order_by('timestamp')

    def perform_create(self, serializer):
        chat = Chat.objects.get(id=self.kwargs['chat_id'])
        serializer.save(chat=chat, sender=self.request.user)






# from rest_framework import serializers, viewsets
# from .models import ChatRoom, Message
# from .serializers import ChatRoomSerializer, MessageSerializer


# class ChatRoomViewSet(viewsets.ModelViewSet):
#     queryset = ChatRoom.objects.all()
#     serializer_class = ChatRoomSerializer

# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

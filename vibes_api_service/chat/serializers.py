from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'sender_username', 'content', 'timestamp', 'is_read']

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = serializers.SlugRelatedField(
        many=True,
        slug_field='id',
        queryset=User.objects.all()
    )

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at']

    def validate_participants(self, value):
        # Ensure exactly two participants
        if len(value) != 2:
            raise serializers.ValidationError("A chat must have exactly two participants.")
        return value










# from rest_framework import serializers
# from .models import ChatRoom, Message


# class ChatRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ChatRoom
#         fields = '__all__'

# class MessageSerializer(serializers.ModelSerializer):
#     sender_username = serializers.CharField(source='sender.username', read_only=True)

#     class Meta:
#         model = Message
#         fields = '__all__'

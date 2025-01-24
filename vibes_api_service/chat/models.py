from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between: {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"







# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ChatRoom(models.Model):
#     participants = models.ManyToManyField(User, related_name="chatrooms")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"ChatRoom {self.id} ({', '.join([user.username for user in self.participants.all()])})"

# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
#     room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Message from {self.sender.username} in Room {self.room.id} at {self.timestamp}"

from django.db import models
from users.models import CustomUser

class ChatRoom(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='chatroom_user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chatroom_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_other_user(self, current_user):
        if self.user1 == current_user:
            return self.user2
        elif self.user2 == current_user:
            return self.user1
        else:
            return None

    def __str__(self):
        return f"Chat between {self.user1.email} and {self.user2.email}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

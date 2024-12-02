from rest_framework import serializers
from chat.models import ChatRoom, Message
from django.contrib.auth.models import User
from users.api.serializers import ProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ChatRoomSerializer(serializers.ModelSerializer):
    user1 = serializers.SerializerMethodField()
    user2 = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user2', 'created_at', 'messages']

    def get_user1(self, obj):
        user = obj.user1

        user_serializer = ProfileSerializer(user)

        return user_serializer.data
    
    def get_user2(self, obj):
        user = obj.user2

        user_serializer = ProfileSerializer(user)

        return user_serializer.data

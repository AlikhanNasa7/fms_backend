from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from chat.models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(user1=user) | ChatRoom.objects.filter(user2=user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a specific chat room"""
        chat_room = self.get_object()
        messages = Message.objects.filter(chat_room=chat_room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        user = self.request.user

        # Check if the user is part of the chat room
        chat_room = ChatRoom.objects.filter(
            id=chat_id
        ).filter(
            Q(user1=user) | Q(user2=user)
        ).first()

        # if not chat_room:
        #     # User is not part of the chat room
        #     raise PermissionDenied("You do not have access to this chat room.")

        # Return messages ordered by timestamp
        return Message.objects.filter(chat_room=chat_room).order_by('timestamp')
    
    def perform_create(self, serializer):
        chat_room = get_object_or_404(ChatRoom, id=self.kwargs['chat_room_id'])
        serializer.save(chat_room=chat_room, sender=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message to a specific chat room"""
        chat_room = self.get_object()
        content = request.data.get('content')

        # Ensure that the current user is either the farmer or the buyer in the chat room
        if chat_room.farmer != request.user and chat_room.buyer != request.user:
            return Response({'detail': 'You are not a participant in this chat room.'}, status=403)

        message = Message.objects.create(chat_room=chat_room, sender=request.user, content=content)
        return Response(MessageSerializer(message).data)


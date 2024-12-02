import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from users.models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']

        chat_room = await self.get_chat_room(self.chat_room_id)

        self.other_user = await self.get_other_user(chat_room, self.user)
        # Ensure chat room exists
        await self.channel_layer.group_add(
            self.chat_room_id,
            self.channel_name
        )

        await self.accept()

        self.send(text_data=json.dumps({
            "type": "connection established",
            "message": "You are now connected"
        }))

    @database_sync_to_async
    def get_chat_room(self, chat_room_id):
        try:
            return ChatRoom.objects.get(id=chat_room_id)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def get_other_user(self, chat_room, current_user):
        return chat_room.get_other_user(current_user)

    async def receive(self, text_data):
        """ Receive message from WebSocket """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to the database
        await sync_to_async(self.save_message)(message)

        # Send message to WebSocket
        await self.channel_layer.group_send(
            self.chat_room_id,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.user_id
            }
        )

    def save_message(self, message):
        """ Save the message to the database """
        chat = ChatRoom.objects.get(pk=self.chat_room_id)
        print(self.user)
        #user = CustomUser.objects.get(pk=token['user_id'])
        Message.objects.create(
            chat_room=chat,
            sender=user,
            content=message
        )

    async def chat_message(self, event):
        """ Send message to WebSocket """
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    async def disconnect(self, close_code):
        """ Leave the group when WebSocket is closed """
        await self.channel_layer.group_discard(
            self.chat_room_id,
            self.channel_name
        )

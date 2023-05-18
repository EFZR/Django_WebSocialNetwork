import json, datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from website.models import *
from Logging.Logger_Base import log

# The AsyncWebsocketConsumer is a class that we can use to create a consumer that will handle websocket connections.
# we use async with the async version of Django
# To enter to the websocket protocol we would use javascript, const socket = new WebSocket('...')


class ChatFriendConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']

        self.chatroom = await self.get_chatroom()
        self.room_group_name = f'chat_{self.chatroom.id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }))

    @database_sync_to_async
    def get_chatroom(self):
        try:
            return ChatRoom.objects.get(id=self.chatroom_id)
        except StopConsumer as e:
            log.error(f"error: {e}")
            messages.error("Something went wrong, please try again later.")
            redirect('website:home')

    @database_sync_to_async
    def save_message(self, message):
        try:
            user = User.objects.get(username=self.scope['user'])
            Message.objects.create(
                chatroom=self.chatroom,
                author=user,
                content=message
            )
        except StopConsumer as e:
            log.error(f"error: {e}")
            messages.error("Something went wrong, please try again later.")
            redirect('website:home')

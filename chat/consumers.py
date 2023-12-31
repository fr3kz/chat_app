import json
import asyncio
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from users.models import User
from .models import Lobby, Message


class ChatConsumer(AsyncWebsocketConsumer):
    connected_users = set()

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]

        if self.user_id not in self.connected_users:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            self.connected_users.add(self.user_id)

            await self.accept()
            lobby_exists = await self.check_if_lobby_exists()
            if not lobby_exists:
                await self.send(text_data=json.dumps({"message": "No such lobby"}))
            else:
                await self.add_user_to_lobby()

                self.last_message_id = None
                asyncio.ensure_future(self.check_messages_periodically())

    async def disconnect(self, close_code):
        await self.remove_user_from_lobby()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        self.connected_users.discard(self.user_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.add_message(message)

    async def check_messages_periodically(self):
        while True:
            messages = await self.get_new_messages()

            if messages:
                await self.get_all_messages(messages)

            await asyncio.sleep(2)

    @database_sync_to_async
    def get_new_messages(self):
        lobby = Lobby.objects.prefetch_related('message_set').get(id=self.room_name)

        if self.last_message_id:
            messages = (
                lobby.message_set
                .filter(id__gt=self.last_message_id)
                .values('id', 'message', 'user__username', 'timestamp')
            )
        else:
            messages = (
                lobby.message_set
                .all()
                .values('id', 'message', 'user__username', 'timestamp')
            )

        if messages:
            self.last_message_id = messages.last()['id']

        return messages

    async def get_all_messages(self, messages):
        for message in messages:
            await self.send(text_data=json.dumps({
                "user": message["user__username"],
                "message": message["message"],
                "time": str(message["timestamp"])
            }))

    @database_sync_to_async
    def check_if_lobby_exists(self):
        return Lobby.objects.filter(id=self.room_name).exists()

    @database_sync_to_async
    def add_user_to_lobby(self):
        lobby = Lobby.objects.get(id=self.room_name)
        user = User.objects.get(id=self.user_id)
        lobby.users.add(user)
        lobby.save()

    @database_sync_to_async
    def remove_user_from_lobby(self):
        lobby = Lobby.objects.get(id=self.room_name)
        user = User.objects.get(id=self.user_id)
        lobby.users.remove(user)
        lobby.save()

    @database_sync_to_async
    def add_message(self, message):
        lobby = Lobby.objects.get(id=self.room_name)
        user = User.objects.get(id=self.user_id)
        new_message = Message.objects.create(lobby=lobby, user=user, message=message, timestamp=datetime.now())
        return new_message.id

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "global_chat"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_message_history()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            username = data['username']
            
            # Create datetime object first
            timestamp = timezone.now()
            
            # Save to database
            await self.save_message(username, message, timestamp)
            
            # Send to group with ISO formatted timestamp
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'timestamp': timestamp.isoformat()
                }
            )
            
        except Exception as e:
            print("Error processing message:", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))

    async def send_message_history(self):
        messages = await self.get_recent_messages()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': messages
        }))

    @database_sync_to_async
    def save_message(self, username, message, timestamp):
        ChatMessage.objects.create(
            username=username,
            message=message,
            timestamp=timestamp
        )

    @database_sync_to_async
    def get_recent_messages(self, limit=50):
        messages = ChatMessage.objects.all().order_by('-timestamp')[:limit]
        return [{
            'username': msg.username,
            'message': msg.message,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]
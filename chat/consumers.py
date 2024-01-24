from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class MyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):     
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message", "")

            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )

    async def disconnect(self, close_code):
        '''
        Called when the socket closes
        '''
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
        
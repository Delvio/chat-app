import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        # get nickname from cookie
        nickname = self.scope["cookies"]["nickname"]
        print(nickname)

        await self.accept()

        await self.send(text_data=json.dumps({"message": f"test has joined."}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sent_by = text_data_json["sent_by"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "sent_by": sent_by,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sent_by = event["sent_by"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({"message": message, "sent_by": sent_by})
        )

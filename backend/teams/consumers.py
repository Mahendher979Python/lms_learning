import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CallConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.team_id = self.scope['url_route']['kwargs']['team_id']

        self.room_group_name = f'call_{self.team_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data['message']

        await self.channel_layer.group_send(

            self.room_group_name,

            {
                'type': 'call_message',
                'message': message
            }
        )

    async def call_message(self, event):

        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
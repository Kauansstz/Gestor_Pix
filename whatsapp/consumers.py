from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.numero = self.scope['url_route']['kwargs']['numero']
        self.room_group_name = f"chat_{self.numero}"

        # Adiciona o usuário ao grupo do chat
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensagem = data['mensagem']

        # Envia para todos no grupo (inclusive o próprio)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'mensagem': mensagem
            }
        )

    async def chat_message(self, event):
        mensagem = event['mensagem']

        # Envia a mensagem para o WebSocket
        await self.send(text_data=json.dumps({
            'mensagem': mensagem
        }))

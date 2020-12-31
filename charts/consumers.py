from channels.generic.websocket import AsyncWebsocketConsumer

class FetchConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        self.user = self.scope['user']
        self.session = self.scope['session']
        if self.user.is_authenticated:
            await self.accept()
        else:
            await self.reject()

    async def receive(self, ytid):
        await self.send(text_data="Hello world!")

    async def disconnect(self, close_code):
        pass

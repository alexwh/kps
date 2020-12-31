from channels.generic.websocket import AsyncWebsocketConsumer
from django_q.tasks import async_task

class FetchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # self.user = self.scope['user']
        # self.session = self.scope['session']
        # if self.user.is_authenticated:
        #     await self.accept()
        # else:
        #     await self.reject()

    async def fetch_comments(request):
        async_task('tasks.fetch_comments_ytid',
                   request.user,
                   request.ytid,
                   hook='tasks.websocket_report')

    async def receive(self, ytid):
        await self.send(text_data="Hello world!")

    async def disconnect(self, close_code):
        pass

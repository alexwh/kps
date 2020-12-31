from uuid import uuid4
from channels.generic.websocket import AsyncWebsocketConsumer
from django_q.tasks import async_task
from asgiref.sync import sync_to_async

class FetchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ytid = self.scope["url_route"]["kwargs"]["ytid"]
        self.user = self.scope["user"]
        self.session = self.scope["session"]
        if self.user.is_authenticated:
            ws_user_id = str(self.user.id)
        else:
            ws_user_id = str(self.user) + str(uuid4())

        self.session["ws_user_id"] = ws_user_id
        self.group_name = ws_user_id
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name)

        await sync_to_async(self.session.save)()
        await self.accept()

    async def fetch_comments(self, request):
        async_task("tasks.fetch_comments_ytid",
                   request.user,
                   request.ytid,
                   hook=self.websocket_report)

    async def websocket_report(self, task):
        if task.success:
            self.send("fetched", task.result)
        else:
            self.send("did not fetch", task.result)

    async def receive(self, text_data=None):
        self.session["timestamp"] = 10000
        await sync_to_async(self.session.save)()
        await self.send("fetch_for " + str(self.session.items()))

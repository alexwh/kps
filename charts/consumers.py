from channels.generic.websocket import WebsocketConsumer
from django_q.tasks import async_task
from . import models

class FetchConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.ytid = self.scope["url_route"]["kwargs"]["ytid"]
        self.stream = models.Stream(stream_id=self.ytid)
        self.accept()

    def fetch_comments(self):
        async_task("charts.tasks.fetch_comments_ytid",
                   self.user,
                   self.ytid)

    def websocket_report(self, task):
        if task.success:
            self.send("fetched", task.result)
        else:
            self.send("did not fetch", task.result)

    def receive(self, text_data=None):
        self.fetch_comments()
        # await self.send(str(dir(self.stream.objects)))
        self.send("yea")

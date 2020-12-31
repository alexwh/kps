from django_q.tasks import async_task
import chat_replay_downloader

def fetch_comments_ytid(user, ytid):
    ytc_dl = chat_replay_downloader.sites.youtube.YouTubeChatDownloader()
    return ytc_dl.get_chat_messages({"url":ytid})

def websocket_report(task):
    if task.success:
        async_task("some.func",
                   "fetched",
                   task.result)
    else:
        async_task("some.func",
                   "did not fetch",
                   task.result)

import chat_replay_downloader
from . import models

def fetch_comments_ytid(user, ytid):
    # channel = models.Channel(user_id="nieuseridlasijdal")
    # stream = models.Stream(stream_id=ytid, channel=channel)
    ytc_dl = chat_replay_downloader.sites.youtube.YouTubeChatDownloader()
    ytc_dl.get_chat_messages({
        "url": ytid,
        "message_groups": ["messages", "superchat"],
        "pause_on_error": True,  # remove later
    })
    # stream.save()

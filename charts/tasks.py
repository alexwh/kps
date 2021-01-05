from datetime import datetime, timedelta, timezone
import chat_replay_downloader
from . import models

def fetch_comments_ytid(user, ytid):
    # channel_user_id =
    channel, _ = models.Channel.objects.get_or_create(user_id="nieuseridlasijdal")
    stream, _ = models.Stream.objects.get_or_create(stream_id=ytid, channel=channel)

    ytc_dl = chat_replay_downloader.sites.youtube.YouTubeChatDownloader()
    msgs = ytc_dl.get_chat_messages({
        "url": ytid,
        "message_groups": ["messages", "superchat"],
        "pause_on_error": True,  # remove later
    })

    # commented because we're filtering manually, may need if switching JSONFields
    # for msg in msgs:
    #     # these are over 50% of the json length and are useless to us
    #     # might be better to monkeypatch chat-replay-downloader's remapping
    #     # functionality to just return none on parse_badges and get_thumbnails
    #     # (sites/youtube.py#_REMAPPING)
    #     if msg["author"]["badges"]:
    #         del msg["author"]["badges"]
    #     if msg["author"]["images"]:
    #         del msg["author"]["images"]

    comments = []
    for msg in msgs:
        # hopefully there should be always at least one object, just get the
        # base url and we can add =s64/=s32 where needed to resize rather than
        # storing all representations of resizes
        avatar = msg["author"]["images"][0]["url"].split("=")[0]
        msg_channel, _ = models.Channel.objects.get_or_create(user_id=msg["author"]["id"], name=msg["author"]["name"], avatar=avatar)
        comments.append(models.StreamComment(
            message_id=msg["message_id"],
            message=msg["message"],
            stream=stream,
            channel=msg_channel,
            timestamp=datetime.fromtimestamp(int(msg["timestamp"]) / 1000000.0, tz=timezone.utc),
            relative_time=timedelta(seconds=int(msg["time_in_seconds"])),
        ))
    models.StreamComment.objects.bulk_create(comments, ignore_conflicts=True)

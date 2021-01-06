from functools import lru_cache
from datetime import datetime, timedelta, timezone
import chat_replay_downloader
import environ
import googleapiclient.discovery
from . import models

@lru_cache()
def fetch_info(resource, ytid):
    env = environ.Env(
        DEBUG=(bool, False)
    )
    google_api_key = env("GOOGLE_API_KEY")
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=google_api_key)

    if resource == "videos":
        request = youtube.videos().list(
            part="snippet",
            fields="items(snippet(channelId,title,description,thumbnails/default/url))",
            id=ytid
        )
        response = request.execute()
        video = response["items"][0]["snippet"]
        channel_id = video["channelId"]
        title = video["title"]
        description = video["description"]
        thumbnail = video["thumbnails"]["default"]["url"]

        return channel_id, title, description, thumbnail
    elif resource == "channels":
        request = youtube.channels().list(
            part="snippet",
            fields="items(snippet(title,thumbnails/default/url))",
            id=ytid
        )
        response = request.execute()
        channel = response["items"][0]["snippet"]
        name = channel["title"]
        avatar = channel["thumbnails"]["default"]["url"]

        return name, avatar


def fetch_comments_ytid(user, ytid):
    channel_id, title, description, thumbnail = fetch_info("videos", ytid)
    channel_name, channel_avatar = fetch_info("channels", channel_id)
    channel, _ = models.Channel.objects.get_or_create(
        user_id=channel_id,
        defaults={
            "name":channel_name,
            "avatar":channel_avatar
        })
    stream, created = models.Stream.objects.get_or_create(
        stream_id=ytid,
        defaults={
            "channel":channel,
            "title":title,
            "description":description,
            "thumbnail":thumbnail
        })

    # bail out early if the stream already exists
    if not created:
        return "did not create existing stream"

    ytc_dl = chat_replay_downloader.sites.youtube.YouTubeChatDownloader()
    msgs = ytc_dl.get_chat_messages({
        "url": ytid,
        "message_groups": ["messages", "superchat"],
    })

    comments = []
    try:
        for msg in msgs:
            # hopefully there should be always at least one object, just get the
            # base url and we can add =s64/=s32 where needed to resize rather than
            # storing all representations of resizes
            msg_channel, _ = models.Channel.objects.get_or_create(
                user_id=msg["author"]["id"],
                defaults={
                    "name": msg["author"]["name"],
                    "avatar": msg["author"]["images"][0]["url"].split("=")[0]
                })
            try:
                comments.append(models.StreamComment(
                    message_id=msg["message_id"],
                    message=msg["message"],
                    stream=stream,
                    channel=msg_channel,
                    timestamp=datetime.fromtimestamp(int(msg["timestamp"]) / 1000000.0, tz=timezone.utc),
                    # this could cause issues with negatives - python timedelta
                    # represents them as -1 days and (day seconds) - time_in_seconds
                    relative_time=timedelta(seconds=int(msg["time_in_seconds"])),
                ))
            except KeyError:
                print(msg)
    except chat_replay_downloader.errors.RetriesExceeded:
        return False

    models.StreamComment.objects.bulk_create(comments, ignore_conflicts=True)

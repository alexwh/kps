import chat_replay_downloader

def fetch_comments_ytid(user, ytid):
    ytc_dl = chat_replay_downloader.sites.youtube.YouTubeChatDownloader()
    return ytc_dl.get_chat_messages({"url":ytid})

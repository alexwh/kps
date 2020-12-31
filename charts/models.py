from django.db import models

class Channel(models.Model):
    userid = models.CharField(max_length=24, primary_key=True, unique=True)
    avatar = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

class Stream(models.Model):
    stream_id = models.CharField(max_length=11, primary_key=True, unique=True)
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()
    description = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

class StreamComment(models.Model):
    message_id = models.CharField(max_length=100, primary_key=True, unique=True)  # 100ish, should be 82 + 3 for potential doublepad
    message = models.CharField(max_length=200)
    message_type = models.CharField(max_length=50)

    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name="comments")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    timestamp = models.DateTimeField()
    action_type = models.CharField(max_length=50)
    relative_time = models.DurationField()

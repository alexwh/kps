from django.contrib import admin

from charts.models import Channel, Stream, StreamComment

admin.site.register(Channel)
admin.site.register(Stream)
admin.site.register(StreamComment)

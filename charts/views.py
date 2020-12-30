from chartjs.views.lines import BaseLineOptionsChartView
from django.core import serializers
from django.shortcuts import get_object_or_404
from . import models

class LineChartJSONView(BaseLineOptionsChartView):
    def __init__(self):
        self.stream = get_object_or_404(models.Stream, pk="qhx65-hjJOs")
        # self.stream.streamcomments_set.all()
        # d = chat_replay_downloader.sites.youtube.YouTubeChatDownloader()
        # self.messages = d.get_chat_messages({"url":self.kwargs["ytid"]})
        # data = serializers.serialize("json", models.StreamComments.objects.all())

    def get_options(self):
        """Return options"""
        return {
            "responsive": False,
            "title": {
                "display": True,
                "text": f"Data for {self.stream.channel.avatar} {self.stream.title}"
            },
            "scales": {
                "xAxes": [{
                    "type": "time",
                    "time": {
                        "parser": "x"  # Unix ms timestamp
                    }
                }],
                "yAxes": [{
                    "scaleLabel": {
                        "display": True,
                        "labelString": "comments"
                    }
                }]
            },
            "plugins": {
                "zoom": {
                    "pan": {
                        "enabled": True,
                        "mode": "xy"
                    },
                    "zoom": {
                        "enabled": True,
                        "mode": "xy",
                    }
                }
            }
        }

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["1:00 AM", "1:01 AM", "1:02 AM", "1:03 AM", "1:04 AM", "1:05 AM", "1:06 AM"]

    def get_providers(self):
        """Return names of datasets."""
        return [self.kwargs["ytid"], "kw0", "kw1", "kw2"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]

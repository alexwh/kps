from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse
from chartjs.views.lines import BaseLineOptionsChartView
from . import models, util

class LineChartJSONView(BaseLineOptionsChartView):
    def dispatch(self, request, *args, **kwargs):
        self.stream = get_object_or_404(models.Stream, stream_id=self.kwargs["ytid"])
        self.keywords = self.request.GET.getlist("keywords[]")
        if self.request.GET.getlist("ignoreprestream") == ["true"]:
            self.comments = self.stream.comments.exclude(relative_time__startswith="-")
        else:
            self.comments = self.stream.comments.all()

        first_comment = self.comments[0]
        last_comment = self.comments[len(self.comments) - 1]  # negative index not supported
        self.start_date = first_comment.timestamp.replace(second=0, microsecond=0)
        self.end_date = last_comment.timestamp.replace(second=0, microsecond=0)  # negative index not supported
        self.rel_start_time = first_comment.relative_time
        self.rel_end_time = last_comment.relative_time

        return super().dispatch(request, *args, **kwargs)

    def get_labels(self):
        """Return labels in 1 minute intervals between the first and last comment"""
        return [dt for dt in util.datetime_range(self.rel_start_time, self.rel_end_time)]

    def get_providers(self):
        """Return the overall message rate and any extra search queries"""
        providers = ["Overall"]
        if self.keywords:
            for keyword in self.keywords:
                if keyword:
                    providers.append(f"Keyword: {keyword}")
        return providers

    def get_data(self):
        """Return overall messages and any extra queries as datasets"""
        data = []
        data.append([  # overall messages
            item
            for item in util.value_or_null(
                self.start_date, self.end_date, self.comments, "timestamp"
            )
        ])
        for keyword in self.keywords:
            if keyword:
                data.append([
                    item
                    for item in util.value_or_null(
                        self.start_date, self.end_date, self.comments, "timestamp", "message", keyword
                    )
                ])
        return data

    def get_options(self):
        """Return options"""

        return {
            "responsive": False,
            "title": {
                "display": True,
                "text": f"Data for {self.stream.title}"
            },
            "scales": {
                # "xAxes": [{
                #     "type": "time",
                #     "distribution": "series",
                #     # "time": {
                #     #     "parser": "x"  # Unix ms timestamp
                #     # }
                # }],
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

class IndexView(TemplateView):
    template_name = 'line_chart.html'

def show_streams(request):
    channel_id = request.GET.get("channel_id")
    if channel_id:
        channel = models.Channel.objects.get(user_id=channel_id)
        streams = models.Stream.objects.filter(channel=channel)
    else:
        streams = models.Stream.objects.all()

    return HttpResponse(serializers.serialize("json", streams, fields=("title")))

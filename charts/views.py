from chartjs.views.lines import BaseLineOptionsChartView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['db_streams'] = models.Stream.objects.all()
        return context

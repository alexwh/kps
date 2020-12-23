import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

class index(TemplateView):
    template_name = "chart.html"
def test(req):
    return HttpResponse(json.dumps({"10:00 PM": 1, "11:00 PM": 10}))

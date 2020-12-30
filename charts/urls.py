from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='line_chart.html'), name='line_chart'),
    path('cinfo/<ytid>.json', views.LineChartJSONView.as_view(), name='line_chart_json'),
]

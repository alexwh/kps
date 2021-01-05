from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='line_chart'),
    path('cinfo/<ytid>.json', views.LineChartJSONView.as_view(), name='line_chart_json'),
]

# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from bbq_thermometer.views import DatumViewSet, SessionViewSet
from bbq_thermometer.views import ChartView, ChartData

router = routers.DefaultRouter()
router.register(r'sessions', SessionViewSet)
router.register(r'data', DatumViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^chart/', ChartView.as_view(), name='get_chart_view'),
    url(r'^chart-data/', ChartData.as_view(), name='get_chart_data'),
]

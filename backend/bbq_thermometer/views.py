# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bbq_thermometer.models import Session, Datum
from bbq_thermometer.utilities import convert_celsius_to_fahrenheit
from bbq_thermometer.serializers import DatumSerializer, SessionSerializer
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.utils import timezone
import datetime


CREATE_SESSION_TIMEOUT = 1  # hours


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


    def create(self, request, *args, **kwargs):
        """
        When creating a new session some values are checked so that the new session will only be created if necessary.
        At the moment the only check is time-based: if the create session called is received when less than a certain
        amount of hours has passed, the previous pending session is returned so that it can be resumed. In the future
        checks regarding the device sending data might also be implemented.
        """
        # Overriding the create method
        try:
            latest_session = Session.objects.all().order_by("-start_date", "-id")[0]
            print "latest session!", latest_session
            try:
                latest_entry = Datum.objects.filter(session=latest_session).order_by("-timestamp")[0]
            except IndexError as e:
                # A session has been previously created but it has never been populated. It needs to be deleted
                latest_entry = None
                latest_session.delete()
            if latest_entry is None or ((timezone.localtime(timezone.now()) - latest_entry.timestamp) >
                                                datetime.timedelta(hours=CREATE_SESSION_TIMEOUT)):
                # If the timestamp is not inside the tolerance window we are going to create a new session
                return super(SessionViewSet, self).create(request, *args, **kwargs)
            else:
                # Otherwise we will resume an existing session
                serializer = SessionSerializer(latest_session)
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DatumViewSet(viewsets.ModelViewSet):
    queryset = Datum.objects.all()
    serializer_class = DatumSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("session", "type")


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        request_params = request.query_params
        session = request_params.get("session", None)
        datum_type = request_params.get("type", None)
        is_celsius = request_params.get("isCelsius", 'true') == 'true'  # Celsius or Fahrenheit flag
        sessions = Session.objects.all()

        # Allowing to filter by Data Type
        if datum_type is None or datum_type == "":
            datum_type = Datum.DATUM_CHOICES[0]
        else:
            datum_type = [choice for choice in Datum.DATUM_CHOICES if choice[0] == datum_type][0]

        response = {
            "chart": {
                "type": "line",
                "zoomType": "x",
            },
            "title": {
                "text": ""
            },
            "tooltip": {
                "style": {
                    "fontWeight": "bold",
                    "fontSize": "14px"
                }
            },
            "xAxis": {
                "type": "datetime"
            },
            "legend": {
                "enabled": True
            },
            "series": [],
            "responsive": {
                "rules": [{
                    "condition": {
                        "maxWidth": None
                    },
                    "chartOptions": {
                        "legend": {
                            "itemStyle": {
                                "fontSize": "20px"
                            },
                            "align": "center",
                            "verticalAlign": "bottom",
                            "layout": "horizontal"
                        },
                        "xAxis": [
                            {
                                "labels": {
                                    "style": {
                                        "fontSize": "14px"
                                    },
                                    "x": 0,
                                    "y": None
                                },
                            }
                        ],
                        "yAxis": [
                            {
                                "labels": {
                                "style": {
                                    "fontSize": "14px"
                                },
                                "align": "left",
                                "x": -15,
                                "y": -5
                                },
                                "title": {
                                    "style": {
                                        "fontSize": "18px"
                                    },
                                    "text": datum_type[1] if is_celsius else datum_type[1].replace("(°C)", "(F)"),
                                    "x": -10
                                }
                            }
                         ],
                        "subtitle": {
                            "text": None
                        },
                        "credits": {
                            "enabled": False
                        }
                    }
                }]
            }
        }

        if sessions:
            if session is None or session == "":
                session = Session.objects.all().order_by("-start_date", "-id")[0]
            else:
                session = Session.objects.get(id=session)

            response["title"]["text"] = "Session #{}: {}".format(session.id, session.start_date)
            data = Datum.objects.filter(session=session, type=datum_type[0]).order_by("timestamp")

            probes = set(data.values_list("probe", flat=True))

            for idx, probe in enumerate(list(probes)):
                response["series"].append(
                    {
                        "type": "line",
                        "data": [],
                        "name": u"{}".format(probe)
                    }
                )
                temp_data = []
                for datum in data.filter(probe=probe):
                    if is_celsius:
                        value = datum.value
                    else:
                        value = convert_celsius_to_fahrenheit(datum.value)
                    temp_data.append(
                        {"x": int(datum.timestamp.strftime("%s")) * 1000,  # Javascript timestamp
                         "y": value}
                    )

                response["series"][idx]["data"] = temp_data

        return Response(response)


class ChartView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        return render(request, "chart.html", {})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bbq_thermometer.models import Session, Datum
from bbq_thermometer.serializers import DatumSerializer, SessionSerializer
from rest_framework import viewsets


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    #
    # def create(self, request, *args, **kwargs):
    #     # Overriding the create method
    #     try:
    #         return super(SessionViewSet, self).create(request, *args, **kwargs)
    #     except IntegrityError:
    #         # Found an existing model
    #         session = Session.objects.get(date=datetime.date.today())
    #         serializer = SessionSerializer(session)
    #         return response.Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DatumViewSet(viewsets.ModelViewSet):
    queryset = Datum.objects.all()
    serializer_class = DatumSerializer

    # def create(self, request, *args, **kwargs):
    #     try:
    #         if request.data.get('session', None) is None:
    #             try:
    #                 request.data['session'] = Session.objects.get(date=datetime.date.today()).id
    #             except (IntegrityError, Session.DoesNotExist):
    #                 session = Session.objects.create()
    #                 request.data['session'] = session.id
    #         server_response = super(ReadViewSet, self).create(request, *args, **kwargs)
    #         return server_response
    #     except Exception as e:
    #         print e, type(e)
    #         return response.Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)

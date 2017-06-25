# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from bbq_thermometer.models import Session, Datum


class DatumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datum


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session

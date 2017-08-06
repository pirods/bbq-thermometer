# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from bbq_thermometer.models import Session, Datum


class DatumAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'timestamp', 'type', 'probe')

admin.site.register(Session)
admin.site.register(Datum, DatumAdmin)

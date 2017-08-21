# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Session(models.Model):
    """
    Used to group readings from the same "Session" even if the connection goes down or the endpoint stops receiving
    readings for a while. Some sort of temporal parameter will be used to discriminate between readings that belong
    to a session and readings that belong to a new one.
    """
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return u"{}: {}".format(self.id, self.start_date)


class Datum(models.Model):
    """
    Single datum. It can contain several readings (of different values as well). Each datum must contain the reference
    to the session it belongs to. Please remember that temperatures are always in °C, resistances in Ohms.
    """
    DATUM_CHOICES = (
        ('TI', 'Internal Temperature (°C)'),
        ('TE', 'External Temperature (°C)'),
        ('R', 'Resistance (Ω)')
    )
    session = models.ForeignKey(Session)
    probe = models.CharField(max_length=8, default=None)  # Numeric sequence of the probe
    type = models.CharField(choices=DATUM_CHOICES, max_length=2)
    value = models.FloatField()  # Value received
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "data"

    def __str__(self):
        return unicode(self.id)

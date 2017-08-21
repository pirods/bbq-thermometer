# -*- coding: utf-8 -*-

"""
Utilities module that contains useful functions to somewhat test, initialise and work with the backend.
"""
from django.utils import timezone
import datetime
import django
import math
import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from bbq_thermometer.models import Datum, Session

def generate_random_data(delete_previous=False, sessions_amount=5, data_amount=100, probes_amount=3):
    """
    Generates some random data that populates the models (and the subsequent chart).
    """
    if delete_previous:
        Datum.objects.all().delete()
        Session.objects.all().delete()


    for i in range(sessions_amount):
        start_date = datetime.date.today() - datetime.timedelta(days=(sessions_amount - (i + 1)))
        session = Session.objects.create()
        session.start_date = start_date
        session.save()
        timestamp = datetime.datetime.combine(start_date, datetime.datetime.min.time()) + datetime.timedelta(
            hours=random.randint(10, 20)
        )
        for datum_type_id, datum_type_name in Datum.DATUM_CHOICES:
            for j in range(probes_amount):
                if datum_type_id == 'TI':
                    starting_value = random.randint(50, 100)
                elif datum_type_id == 'TE':
                    starting_value = random.randint(-5, 30)
                elif datum_type_id == 'R':
                    starting_value = random.randint(100000, 125000)
                last_value = starting_value
                for z in range(data_amount):
                    last_value += random.randint(
                        -int(math.ceil(abs(starting_value * 0.1)) + 0.1),
                        int(math.ceil(abs(starting_value * 0.1)) + 0.1)
                    )
                    datum = Datum.objects.create(
                        session=session,
                        probe=j,
                        type=datum_type_id,
                        value=last_value
                    )
                    datum.timestamp = (timestamp + datetime.timedelta(minutes=z)).replace(tzinfo=timezone.get_current_timezone())
                    datum.save()


def convert_celsius_to_fahrenheit(temperature_celsius):
    """
    Simple Celsius to Fahrenheit converter
    """
    return 9.0/5.0 * temperature_celsius + 32

# Uncomment and run to generate some data
# generate_random_data(delete_previous=True)
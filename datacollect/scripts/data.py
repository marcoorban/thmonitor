""" Contains helper functions for the creation and manipulation of sensor
   readings """

from ..models import Sensor, Reading
from datetime import datetime
from django.utils import timezone
import pytz
import zoneinfo


taipei_tz = pytz.timezone("Asia/Taipei")

def create_reading(temp, humi, hi, sensorname, pressure=1000.0):
    sensor = Sensor.objects.get(name=sensorname)
    reading = Reading(temperature=temp,
            humidity=humi,
            heat_index=hi,
            pressure=pressure,
            sensor=sensor,
            time=datetime.now(taipei_tz))
    print(reading)
    return reading

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get("django_timezone")
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)

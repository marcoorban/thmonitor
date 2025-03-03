from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from .models import Room, Sensor, Reading
from datetime import datetime


def index(request):
    sensor_list = Sensor.objects.order_by("name")
    context = {"sensor_list": sensor_list}
    return render(request, "datacollect/index.html", context)


def monitor(request):
    r = request.GET
    temp = float(r["temperature"].strip())
    humi = float(r["humidity"].strip())
    hi = float(r["heat_index"].strip())
    try:
        pres = float(r["pressure"].strip())
    except:
        pres = 1000.0
    sensorname = r["sensor"].strip()
    timestr = r["time"]
    time = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")

    s = Sensor.objects.get(name=sensorname)

    print(time)

    reading = Reading(
        temperature=temp,
        humidity=humi,
        heat_index=hi,
        pressure=pres,
        sensor=s,
        time=time,
    )
    print(reading)
    return HttpResponse("Got data")


def post_data(request):
    pass


def room(request):
    pass


def sensor(request, sensor_id):
    sensor = Sensor.objects.get(sensor_id)
    context = {"sensor": sensor}
    return render(request, reverse("sensor"))
    pass


# Create your views here.

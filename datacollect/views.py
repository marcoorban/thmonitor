"""Views of project"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Sensor, Reading
from .forms import ImportCSVForm

def index(request):
    """ View function for index / home page"""
    sensor_list = Sensor.objects.order_by("name")
    context = {"sensor_list": sensor_list}
    return render(request, "datacollect/index.html", context)


def monitor(request):
    """ Page that shows temperature and humidity data from sensors"""
    r = request.GET
    temp = float(r["temperature"].strip())
    humi = float(r["humidity"].strip())
    hi = float(r["heat_index"].strip())
    try:
        pres = float(r["pressure"].strip())
    except ValueError:
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
    """ This function enables sensors to post their data to the database """
    return request


def room(request):
    """ Shows view with list of rooms and the average sensor readings"""
    return request


def sensor(request, sensor_id):
    """ Shows view with list of sensors and their readings"""
    sensor = Sensor.objects.get(sensor_id)
    context = {"sensor": sensor}
    return render(request, reverse("sensor"))


def import_csv(request):
    """ This view shows a form to import data from .csv file. Useful for data
    that existed before the post_data function was implemented. """
    # This needs a get and a post request

    if request.method == "POST":
        form = ImportCSVForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")
    # If get request, just show the form
    else:
       form = ImportCSVForm()
       return render(request, "datacollect/importcsv.html", {"form":form})
    # If post request, call the import
    # function and import the data


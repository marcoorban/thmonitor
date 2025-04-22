"""Views of project"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Sensor, Reading
from .forms import ImportCSVForm
from .scripts.data import create_reading

READINGS = {"Sensehat":None} # This list will contain the latest readings for each sensor

def index(request):
    """ View function for index / home page"""
    sensor_list = Sensor.objects.order_by("name")
    context = {"sensor_list": sensor_list}
    return render(request, "datacollect/index.html", context)

def test(request):
    """ This is just a test view that sends an HTTP response to test
    if clients are connecting properly """
    content = "You have successfully connected, punk!"
    return HttpResponse(content=content, status=200, content_type="text/html")

def monitor(request):
    """ This view is where the sensors are posting their readings.
    It takes the data given by a sensor and saves it as a reading in
    the database"""

    return render(request, "datacollect/monitor.html", {"readings":READINGS})

def post_data(request):
    """ This function enables sensors to post their data to the database """
    r = request.GET
    # parse the arguments sent by the sensor
    temp = float(r["temperature"].strip())
    humi = float(r["humidity"].strip())
    hi = float(r["heat_index"].strip())
    try:
        pres = float(r["pressure"].strip())
    except:
        pres = 1000.0
    sensorname = r["sensor"].strip()
    # Create (but not save) the reading from the arguments
    reading = create_reading(temp, humi, hi, sensorname, pres) 
    # Update the global READINGS dictionary of sensor readings.
    READINGS[sensorname] = reading
    print(READINGS)
        # Save the reading every five minutes only
    mins = datetime.now().minute
    if mins % 5 == 0:
        reading.save()
        print("Reading saved!")
    return HttpResponse("Got data, thanks!")


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
            upfile = form.csvfile
            # Make sure that the file is indeed a csv
            if not is_csv(upfile):
              pass
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")
        else:
            # Redirect to form site, but show an error.
            pass
    # If get request, just show the form
    else:
       form = ImportCSVForm()
       return render(request, "datacollect/importcsv.html", {"form":form})
    # If post request, call the import
    # function and import the data


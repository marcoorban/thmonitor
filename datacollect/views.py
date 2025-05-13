"""Views of project"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Sensor, Reading
from .forms import ImportCSVForm
from .scripts.data import create_reading
from pathlib import Path

cur_readings = {"Sensehat":[], "DHT11_1":[]} # This list will contain the latest readings for each sensor
cache = {"Sensehat":[], "DHT11_1":[]}
PARENT = Path(__file__).parent.resolve()

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

    return render(request, "datacollect/monitor.html", {"readings":cur_readings})

def post_data(request):
    """ This function writes data from sensors to database """
    r = request.GET
    now = datetime.now()
    # parse the arguments sent by the sensor
    temp = r["temperature"].strip()
    humi = r["humidity"].strip()
    hi = r["heat_index"].strip()
    try:
        pres = r["pressure"].strip()
    except:
        pres = "1000.0"
    sensorname = r["sensor"].strip()

    sensor = Sensor.objects.get(name=sensorname)
    
    # create a reading object
    this_reading = Reading(temperature=temp,
                          humidity=humi,
                          heat_index=hi,
                          pressure=pres,
                          sensor=sensor,
                          time=now)
    global cur_readings
    cur_readings[sensorname] = this_reading

    # Decide whether to add and write to cache depending on the clock time.
    min_now = now.minute
    # add data to cache every five minutes
    if min_now % 5 == 0:
        now_string = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        data = [now_string, temp, humi, hi, pres]
        data_string = ','.join(data)
        add_to_cache(sensorname, data_string)
    # write data to cache every thirty minutes
    if min_now % 30 == 0:
        write_cache(sensorname)

    return HttpResponse("Thanks for the data!")

def add_to_cache(sensorname, data):
    global cache
    cache[sensorname].append(data)

def write_cache(sensorname):
    global cache
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    filename_path = Path(PARENT, "data", sensorname, str(year), str(month))
    filename = Path(filename_path, str(day) + ".csv")

    if not filename_path.exists():
        # Create the directory
        filename_path.mkdir(parents=True, exist_ok=True)
    if not filename.exists():
        # Create the file
        with open(filename, "w") as f:
            f.write("date, temperature, humidity, heat_index, pressure\n")
    with open(filename, "a") as f:
        for line in cache[sensorname]:
            f.write(line + "\n")   
    # delete the cache to start adding data to it
    cache[sensorname] = []

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


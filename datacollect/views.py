from django.shortcuts import render
from django.http import HttpResponse

from .models import Room, Sensor


def index(request):
    sensor_list = Sensor.objects.order_by("name")
    context = {"sensor_list": sensor_list}
    return render(request, "datacollect/index.html", context)


def monitor(request):
    pass


def post_data(request):
    pass


def room(request):
    pass


def sensor(request):
    pass


# Create your views here.

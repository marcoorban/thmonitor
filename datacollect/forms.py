from django import forms
from .models import Sensor

sensors = Sensor.objects.all()
sensor_choices = {sensor.name: sensor.name for sensor in sensors}

class ImportCSVForm(forms.Form):
    csvfile = forms.FileField(label="Csv file")
    sensor = forms.ChoiceField(choices=(sensor_choices), label="Sensor")

from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=32)


class Sensor(models.Model):
    name = models.CharField(max_length=32)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class Reading(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    heat_index = models.FloatField()
    pressure = models.FloatField(blank=True, default=1000.0)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)

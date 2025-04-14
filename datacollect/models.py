from django.db import models

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=32)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} @ {self.room.name}"


class Reading(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    heat_index = models.FloatField()
    pressure = models.FloatField(blank=True, default=1000.0)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return f"T:{self.temperature}, H:{self.humidity}, FL:{self.heat_index}\n From {self.sensor} @ {self.time}"

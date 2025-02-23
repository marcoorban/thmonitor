from django.contrib import admin

# Register your models here.

from .models import Room, Sensor, Reading

admin.site.register(Room)
admin.site.register(Sensor)
admin.site.register(Reading)

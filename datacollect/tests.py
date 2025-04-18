from django.test import TestCase
from datacollect.scripts.data import save_reading 
from datacollect.models import Room, Sensor, Reading
from datetime import datetime

class SaveReadingTestCase(TestCase):
    def setUp(self):
        test_room = Room.objects.create(name="TestRoom")
        test_sensor = Sensor.objects.create(name="TestSensor", room=test_room)

    def test_reading_created(self):
        test_sensor = Sensor.objects.get(name="TestSensor")
        temp = 100
        humi = 43.4
        hi = 23.1
        pressure = 1000.0
        time = datetime.now()
        test_reading_1 = Reading.objects.create(temperature=temp,
                                                humidity=humi,
                                                heat_index=hi,
                                                pressure=pressure,
                                                sensor=test_sensor,
                                                time=time)
        readings = Reading.objects.all()
        self.assertEqual(len(readings), 1)
        self.assertEqual(test_reading_1.temperature, 100)

    def test_reading_saved(self):
        """ Tests the function in the helper script that takes readings from
        sensors and saves them to the database"""
        sensorname = "TestSensor"
        temp = 111.1
        humi = 123.1
        hi = 123.4
        pressure = 1000.1
        test_reading = save_reading(temp, humi, hi, sensorname, pressure)
        test_reading2 = save_reading(temp+200, humi, hi, sensorname, pressure)
        readings = Reading.objects.all()
        self.assertEqual(len(readings), 2)
        self.assertEqual(test_reading.pressure, 1000.1)

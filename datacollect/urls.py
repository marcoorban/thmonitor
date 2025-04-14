from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("monitor/", views.monitor, name="monitor"),
    path("post_data/", views.post_data, name="post_data"),
    path("room/<int:room_id>/", views.room, name="room"),
    path("sensor/<int:sensor_id>/", views.sensor, name="sensor"),
    path("import", views.import_csv, name="import"),
]

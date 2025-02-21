from typing import Optional
from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as so
from server import db

class Room(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, 
                                            unique=True)
    
    def __repr__(self):
        return '<Room {}>'.format(self.name)
    

class Sensor(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                            unique=True)
    room: so.Mapped[Room] = so.mapped_column(sa.ForeignKey(Room.id),
                                             index=True)
    readings: so.WriteOnlyMapped['Reading'] = so.relationship(back_populates='sensed_by')
    
    def __repr__(self):
        return '<Sensor {} @ {}>'.format(self.name, self.room)
    
class Reading(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    temperature: so.Mapped[float] = so.mapped_column()
    humidity: so.Mapped[float] = so.mapped_column()
    pressure: so.Mapped[Optional[float]] = so.mapped_column()
    heat_index: so.Mapped[float] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True)
    sensor: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Sensor.id),
                                              index=True)
    sensed_by: so.Mapped[Sensor] = so.relationship(back_populates='readings')
    
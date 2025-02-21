from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from server import db

class Room(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, 
                                            unique=True)
    
    def __repr__(self):
        return '<Room {}>'.format(self.name)

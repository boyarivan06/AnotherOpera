from typing import Any

from sqlalchemy import Column, Text, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    duration = Column(Integer)
    artist = Column(String)
    record = Column(String)
    file_path = Column(String)

    def __str__(self):
        return f'{self.name} by {self.artist}'

    def get_dict(self):
        return {'name':self.name, 'artist':self.artist, 'duration':self.duration, 'record':self.record, 'file_path':self.file_path}

    @classmethod
    def load(cls, data:dict[str, Any]):
        new_s = Song()
        for k in data:
            new_s.__dict__[k] = data[k]
        return new_s
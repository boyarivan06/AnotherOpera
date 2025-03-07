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
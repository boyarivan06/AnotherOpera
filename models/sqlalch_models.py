from typing import Any

from special import log_action, MetaControl
from api import APIConnect


class Descriptor(metaclass=MetaControl):
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Song(APIConnect, metaclass=MetaControl):
    name: Descriptor()
    duration: Descriptor()
    artist: Descriptor()
    record: Descriptor()
    file_path: Descriptor()
    slots = ['name', 'duration', 'artist', 'record', 'file_path']

    @log_action
    def __init__(self, name='empty', duration=None, artist=None, record=None, file_path=None):
        self.artist = artist
        self.name = name
        self.duration = duration
        self.file_path = file_path
        self.record = record

    def __str__(self):
        return f'{self.name} by {self.artist}'
    @log_action
    def get_dict(self):
        return {'name':self.name, 'artist':self.artist, 'duration':self.duration, 'record':self.record, 'file_path':self.file_path}


class Artist(APIConnect, metaclass=MetaControl):
    name = Descriptor()
    type = Descriptor()
    image_path = Descriptor()

    @log_action
    def __init__(self, name='empty', type=None, image_path=None):
        self.type = type
        self.name = name
        self.image_path = image_path


class Record(APIConnect, metaclass=MetaControl):
    name = Descriptor()
    artist = Descriptor()
    type = Descriptor()
    genre = Descriptor()
    @log_action
    def __init__(self, name='empty', artist=None, type=None, genre=None):
        self.name = name
        self.artist = artist
        self.type = type
        self.genre = genre

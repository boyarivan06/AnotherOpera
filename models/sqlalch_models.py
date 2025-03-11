from typing import Any

from special import log_action, MetaControl


class Descriptor:
    __metaclass__ = MetaControl
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Song:
    __metaclass__ = MetaControl
    name: Descriptor()
    duration: Descriptor()
    artist: Descriptor()
    record: Descriptor()
    file_path: Descriptor()
    slots = ['name', 'duration', 'artist', 'record', 'file_path']
    @log_action
    def __init__(self, name, duration, artist, record, file_path):
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

    @classmethod
    def load(cls, data:dict[str, Any]):
        new_s = Song(None, None, None, None, None)
        for k in data:
            new_s.__dict__[k] = data[k]
        return new_s
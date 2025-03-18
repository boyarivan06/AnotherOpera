import audioread

from special import log_action, MetaControl
from api import APIConnect


class Descriptor(metaclass=MetaControl):
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Track(APIConnect, metaclass=MetaControl):
    id = Descriptor()
    name: Descriptor()
    album_id = Descriptor()
    album_name = Descriptor()
    artist_id = Descriptor()
    artist_name = Descriptor()
    album_image = Descriptor()
    audio = Descriptor()
    duration = Descriptor()
    slots = ['id', 'name', 'album_id', 'album_name', 'artist_id', 'artist_name', 'album_image', 'audio', 'duration']

    ''''@log_action
    def __init__(self, name='empty', duration=None,
                 artist=None, record=None, file_path=None):
        self.artist = artist
        self.name = name
        self.duration = duration
        self.file_path = file_path
        self.record = record'''
    def __init__(self, data):
        super().__init__(data)
        self.duration *= 1000


    def __str__(self):
        return f'{self.name} by {self.artist_name}'
    @log_action
    def get_dict(self):
        return {'name':self.name, 'artist':self.artist_name,
                'record':self.album_name,
                'file_path':self.audio}


class Artist(APIConnect, metaclass=MetaControl):
    id = Descriptor()
    name = Descriptor()
    image = Descriptor()
    slots = ['id', 'name', 'image']


class Album(APIConnect, metaclass=MetaControl):
    id = Descriptor()
    name = Descriptor()
    artist_id = Descriptor()
    artist_name = Descriptor()
    image = Descriptor()
    slots = ['id', 'name', 'artist_id', 'artist_name', 'image']

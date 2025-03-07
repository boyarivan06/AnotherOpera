import gc
import json
from datetime import datetime
from json import JSONEncoder

from custom_exc import DurationException


class SingleTon:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance


class SongDataBase(SingleTon):
    data: list
    def append(self, song: 'BaseSong'):
        self.data.append(song)

    def __getitem__(self, index):
        return self.data[index]

    def __get__(self, instance, owner):
        return instance.data


class Descriptor:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class BaseSong:
    __created: str
    name: Descriptor()
    duration: Descriptor()
    artist: Descriptor()
    music_author: Descriptor()
    genre: Descriptor()

    def __init__(self, name, duration, music_author, genre):
        if duration <= 0:
            raise DurationException
        self.name = name
        self.duration = duration
        self.music_author = music_author
        self.genre = genre
        self.__created = datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')

    @property
    def created(self):
        return self.__created

    def __str__(self):
        return f"""{self.name}
music by {self.music_author}
duration: {self.duration}
genre: {self.genre}"""

    @classmethod
    def get_all(cls):
        return [f'"{ob.name}" ({ob.__class__.__name__})' for ob in gc.get_objects() if isinstance(ob, BaseSong)]


class SongEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class VocalSong(BaseSong):
    text = Descriptor()
    singer = Descriptor()
    text_author: Descriptor()

    def __init__(self, name, duration, music_author, genre, text, singer, text_author):
        super().__init__(name, duration, music_author, genre)
        self.text = text
        self.singer = singer
        self.text_author = text_author

    def __str__(self):
        return super().__str__() + f"""
singer: {self.singer}
text by: {self.text_author}
text:
{self.text}"""


class InstrumentalSong(BaseSong):
    main_instrument: Descriptor()

    def __init__(self, name, duration, music_author, genre, main_instrument):
        super().__init__(name, duration, music_author, genre)
        self.main_instrument = main_instrument

    def __str__(self):
        return super().__str__() + f"""
        main instrument: {self.main_instrument}"""

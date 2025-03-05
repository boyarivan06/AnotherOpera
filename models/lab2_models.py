import gc
from datetime import datetime

from custom_exc import DurationException


class Descriptor:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class BaseSong:
    __created: datetime
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
        self.__created = datetime.now()

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
        for ob in gc.get_objects():
            if isinstance(ob, BaseSong):
                print(f'"{ob.name}" ({ob.__class__.__name__})')

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

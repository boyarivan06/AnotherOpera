from datetime import date


class Song:
    _name: str
    _duration: float
    _artist: 'Artist'
    _record: 'Record'

    def __init__(self, name, artist, record, duration):
        self.name = name
        self.artist = artist
        self.record = record
        self.duration = duration

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def artist(self) -> 'Artist':
        return self._artist

    @property
    def record(self) -> 'Record':
        return self._record

    @property
    def duration(self) -> float:
        return self._duration

    @artist.setter
    def artist(self, value: 'Artist'):
        self._artist = value

    @record.setter
    def record(self, value: 'Record'):
        self._record = value

    @duration.setter
    def duration(self, value: float):
        self._duration = value


class Artist:
    _name: str
    _type: str
    _genres: list['Genre']

    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value:str):
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, value: list):
        self._genres = value

    def __str__(self):
        return self.name


class Record:
    _name: str
    _artist: 'Artist'
    _date: date
    _type: str  # single, EP, LP
    _genre: 'Genre'

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def artist(self) -> 'Artist':
        return self._artist

    @artist.setter
    def artist(self, value: 'Artist'):
        self._artist = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value: 'Genre'):
        self._genre = value

    @property
    def date(self):
        return self._date

    @genre.setter
    def genre(self, value: date):
        self._date = value


class Genre:
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

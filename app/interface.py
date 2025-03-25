from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtCore, QtMultimedia

from utils.api import APIConnect
from utils.custom_exc import APIFailException
from utils.special import log_action
from utils.models import Track, Album, Artist


class App(QMainWindow):
    player = None
    playing = False
    started = False
    stop_position = 0
    current_artist = None
    current_album = None

    @log_action
    def __init__(self):
        super().__init__()
        uic.loadUi("QT_windows/main.ui", self)
        # self.add_song_button.clicked.connect(self.create_song_dialog)
        self.get_artists()  # TODO: make async
        self.songs_list.itemClicked.connect(self.show_song)
        self.artists_list.itemClicked.connect(self.get_albums)
        self.albums_list.itemClicked.connect(self.get_songs)
        self.artist_search.textEdited.connect(self.search_artist)
        self.album_search.textEdited.connect(self.search_album)
        self.song_search.textEdited.connect(self.search_song)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.positionChanged.connect(self.position_changed)
        self.song_slider.valueChanged.connect(self.slider_moved)
        self.play_stop_button.clicked.connect(self.play_stop)

    def warn(self, text):
        self.warning_label.setText(text)

    def dewarn(self):
        self.warning_label.setText("")

    def change_song(self, song):
        url = QtCore.QUrl(song.audio)
        content = QtMultimedia.QMediaContent(url)
        self.player.stop()
        self.player.setMedia(content)
        self.playing = False
        self.play_stop_button.setText("PLAY")
        self.player.setPosition(1)
        self.started = False

    @log_action
    def slider_moved(self, value):
        self.player.setPosition(value)

    @log_action
    def position_changed(self, position):
        if self.playing:
            self.song_slider.setSliderPosition(position)

    @log_action
    def get_albums(self, item, search=""):
        try:
            self.current_artist = Artist.get_one(
                name=(item.text() if not isinstance(item, APIConnect) else item.name)
            )
        except APIFailException:
            self.warn("Артист не найден")
            return
        try:
            albums = Album.get_all(
                artist_name=self.current_artist.name, namesearch=search
            )
        except APIFailException:
            self.warn("Альбом не найден")
            return
        self.albums_list.clear()
        self.albums_list.addItems([e.name for e in albums])

    def search_artist(self):
        search = self.artist_search.text()
        self.get_artists(search=search)

    def search_album(self):
        search = self.album_search.text()
        self.get_albums(self.current_artist, search=search)

    def search_song(self):
        search = self.artist_search.text()
        self.get_songs(self.current_album, search=search)

    @log_action
    def get_artists(self, search=""):
        self.dewarn()
        try:
            artists = Artist.get_all(namesearch=search)
        except APIFailException:
            self.warn("Артист не найден")
            return
        self.artists_list.clear()
        self.artists_list.addItems([e.name for e in artists])

    @log_action
    def get_songs(self, item, search=""):
        self.dewarn()
        try:
            self.current_album = Album.get_one(
                name=(item.text() if not isinstance(item, APIConnect) else item.name)
            )
        except APIFailException:
            self.warn("Альбом не найден")
            return
        if not self.current_album:
            return
        try:
            songs = Track.get_all(album_name=self.current_album.name)
        except APIFailException:
            self.warn("Песни не найдены")
            return
        self.songs_list.clear()
        self.songs_list.addItems([e.name for e in songs])

    @log_action
    def show_song(self, item):
        self.dewarn()
        song = None
        try:
            song = Track.get_one(name=item.text(), artist_name=self.current_artist.name)
        except APIFailException or not song:
            self.warn("Песня не найдена")
            return
        self.change_song(song)
        self.song_slider.setMaximum(song.duration)
        self.song_slider.setSliderPosition(1)
        self.name_label.setText(song.name)
        self.artist_label.setText(song.artist_name)
        self.record_label.setText(song.album_name)

    def play_stop(self):
        if not self.playing:
            if not self.started:
                self.started = True
            else:
                self.player.setPosition(self.stop_position)
            self.player.play()
            self.playing = True
            self.play_stop_button.setText("STOP")

        else:
            self.stop_position = self.player.position()
            self.playing = False
            self.player.stop()
            self.play_stop_button.setText("PLAY")

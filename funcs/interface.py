import os
import shutil

# import audioread
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5 import uic, QtCore, QtMultimedia

from api import APIConnect
from special import log_action
from models import Track, Album, Artist
from config import MEDIA_ROOT


class ConfirmDialog(QDialog):
    @log_action
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('QT_windows/confirm.ui', self)
        self.buttonBox.accepted.connect(self.accepted)
        self.acc = False

    @log_action
    def accepted(self):
        self.acc = True


class NewSongForm(QDialog):
    filename: str|None
    @log_action
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('QT_windows/new_song.ui', self)
        self.buttonBox.accepted.connect(self.create_song)
        # self.file_button.clicked.connect(self.get_file)
        self.filename = None

    @log_action
    def create_song(self):
        #if self.filename is None:
        #    self.warning_label.setText('файл не выбран!')
        #    return
        dur = .0
        #with audioread.audio_open(self.filename) as ex:
        #    dur = int(ex.duration * 1000)  # in microseconds
        name = self.name_input.text() if self.name_input.text() \
            else self.filename.split('/')[-1].split('.')[0]
        #s = Track(name=name, duration=dur,
        #             artist=self.artist_input.text(),
        #         record=self.record_input.text(), file_path=self.filename)
        #s.new_object()
        #self.close()

    @log_action
    def get_file(self):
        # fd = QFileDialog(self)
        # fd.exec()
        file_path = QFileDialog.getOpenFileName(self, 'Open file',
                                                os.path.abspath('Downloads'),
                                                "Audio files (*.mp3 *.wav)")
        # print(filename)
        self.file_label.setText(file_path[0].split('/')[-1])
        shutil.copyfile(file_path[0], os.path.join(MEDIA_ROOT,
                                                   file_path[0].split('/')[-1]))
        self.filename = str(os.path.join(MEDIA_ROOT, file_path[0].split('/')[-1]))
        self.warning_label.setText('')

class SelectSongDialog(QDialog):
    @log_action
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('QT_windows/select_song.ui', self)
        self.buttonBox.accepted.connect(self.selected)

    @log_action
    def selected(self):
        form = NewSongForm(self)
        form.exec()


class SongView(QDialog):
    player = None
    playing = False
    started = False
    stop_position = 0

    @log_action
    def __init__(self, parent, player, song: Track):
        super().__init__(parent)
        uic.loadUi('QT_windows/song_view.ui', self)
        if player:
            self.play_stop_button.clicked.connect(self.play_stop)
            self.playing = False
            self.player = player
            self.player.positionChanged.connect(self.position_changed)
            self.song_slider.valueChanged.connect(self.slider_moved)
            self.song_slider.setMaximum(song.duration)
        # self.del_button.clicked.connect(self.delete_song)
        self.song = song

    def delete_song(self):
        confirm_dialog = ConfirmDialog(self)
        confirm_dialog.exec()
        if confirm_dialog.acc:
            # os.remove(self.song.file_path)
            self.song.delete_object()
            self.parent().refresh_list()
            self.close()


    def play_stop(self):
        if not self.playing:
            if not self.started:
                self.started = True
            else:
                self.player.setPosition(self.stop_position)
            self.player.play()
            self.playing = True
            self.play_stop_button.setText('STOP')

        else:
            self.stop_position = self.player.position()
            self.playing = False
            self.player.stop()
            self.play_stop_button.setText('PLAY')



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
        uic.loadUi('QT_windows/main.ui', self)
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


    def change_song(self, song):
        url = QtCore.QUrl(song.audio)
        content = QtMultimedia.QMediaContent(url)
        self.player.stop()
        self.player.setMedia(content)
        self.playing = False
        self.play_stop_button.setText('PLAY')
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
    def get_albums(self, item, search=''):
        self.current_artist = Artist.get_one(name=(item.text() if not isinstance(item, APIConnect) else item.name))
        albums = Album.get_all(artist_name=self.current_artist.name, namesearch=search)
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
    def get_artists(self, search=''):
        artists = Artist.get_all(namesearch=search)
        self.artists_list.clear()
        self.artists_list.addItems([e.name for e in artists])


    @log_action
    def get_songs(self, item, search=''):
        self.current_album = Album.get_one(name=(item.text() if not isinstance(item, APIConnect) else item.name))
        if not self.current_album:
            return
        songs = Track.get_all(album_name=self.current_album.name)
        self.songs_list.clear()
        self.songs_list.addItems([e.name for e in songs])

    def create_song_dialog(self):
        dialog = NewSongForm(self)
        dialog.exec()
        self.refresh_list()

    @log_action
    def show_song(self, item):
        song = Track.get_one(name=item.text(), artist_name=self.current_artist.name)
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
            self.play_stop_button.setText('STOP')

        else:
            self.stop_position = self.player.position()
            self.playing = False
            self.player.stop()
            self.play_stop_button.setText('PLAY')

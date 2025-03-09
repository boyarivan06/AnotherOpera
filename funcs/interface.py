import os

import audioread
from PyQt5.QtWidgets import QMainWindow, QDialog, QFileDialog
from PyQt5 import uic, QtMultimedia, QtCore
from funcs.scripts.db import session
from models.sqlalch_models import Song
from config import MEDIA_ROOT


class ConfirmDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('QT_windows/confirm.ui', self)
        self.buttonBox.accepted.connect(self.accepted)
        self.acc = False

    def accepted(self):
        self.acc = True


class NewSongForm(QDialog):
    filename: str|None
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('QT_windows/new_song.ui', self)
        self.buttonBox.accepted.connect(self.create_song)
        self.file_button.clicked.connect(self.get_file)
        self.filename = None

    def create_song(self):
        if self.filename is None:
            self.warning_label.setText('файл не выбран!')
            return
        dur = .0
        name = '--song-name--'
        with audioread.audio_open(self.filename) as ex:
            dur = int(ex.duration * 1000)
        name = self.name_input.text() if self.name_input.text() else self.filename.split('/')[-1].split('.')[:-1]
        s = Song(name=name, duration=dur,
                     artist=self.artist_input.text(),
                 record=self.record_input.text(), file_path=self.filename)
        session.add(s)
        session.commit()
        self.close()

    def get_file(self):
        # fd = QFileDialog(self)
        # fd.exec()
        file_path = QFileDialog.getOpenFileName(self, 'Open file', os.path.abspath('Downloads'), "Audio files (*.mp3 *.wav)")
        # print(filename)
        self.file_label.setText(file_path[0].split('/')[-1])
        os.rename(file_path[0], os.path.join(MEDIA_ROOT, file_path[0].split('/')[-1]))
        self.filename = str(os.path.join(MEDIA_ROOT, file_path[0].split('/')[-1]))
        self.warning_label.setText('')

class SelectSongDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('QT_windows/select_song.ui', self)
        self.buttonBox.accepted.connect(self.selected)

    def selected(self):
        form = NewSongForm(self)
        form.exec()


class SongView(QDialog):
    player = None
    playing = False
    started = False
    stop_position = 0
    def __init__(self, parent, player, song):
        super().__init__(parent)
        uic.loadUi('QT_windows/song_view.ui', self)
        self.play_stop_button.clicked.connect(self.play_stop)
        self.playing = False
        self.player = player
        self.player.positionChanged.connect(self.position_changed)
        self.song_slider.valueChanged.connect(self.slider_moved)
        self.song_slider.setMaximum(song.duration)
        self.del_button.clicked.connect(self.delete_song)
        self.song = song

    def delete_song(self):
        confirm_dialog = ConfirmDialog(self)
        confirm_dialog.exec()
        if confirm_dialog.acc:
            os.remove(self.song.file_path)
            session.delete(self.song)
            session.commit()
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

    def slider_moved(self, value):
        """
        slider moves from 0 to 100 !!!
        :param value: current position of the slider
        """
        self.player.setPosition(value)

    def position_changed(self, position):
        if self.playing:
            self.song_slider.setSliderPosition(position)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('QT_windows/main.ui', self)
        self.add_song_button.clicked.connect(self.create_song_dialog)
        self.refresh_list()
        self.songs_list.itemClicked.connect(self.show_song)

    def create_song_dialog(self):
        dialog = NewSongForm(self)
        dialog.exec()
        self.refresh_list()

    def show_song(self, item):
        song = session.query(Song).filter(Song.name==item.text()).first()
        if not song:
            print(f"AAAAAAAA `{item.text()}`")
            return
        url = QtCore.QUrl.fromLocalFile(song.file_path)
        content = QtMultimedia.QMediaContent(url)
        player = QtMultimedia.QMediaPlayer()
        player.setMedia(content)
        dialog = SongView(self, player, song)
        dialog.name_label.setText(song.name)
        dialog.artist_label.setText(song.artist)
        dialog.duration_label.setText(str(song.duration))
        dialog.duration = song.duration
        dialog.record_label.setText(song.record)
        dialog.setWindowTitle(song.name)

        if not player:
            print('aaa, no player!!!')
        dialog.player = player
        dialog.exec()

    def refresh_list(self):
        self.songs_list.clear()
        self.songs_list.addItems([e.name for e in session.query(Song).all()])
import sys

import audioread
from PyQt5.QtWidgets import QWidget, QMainWindow, QDialog, QFileDialog
from PyQt5 import uic, QtMultimedia, QtCore
from db import session
from models.sqlalch_models import Song


class SongForm(QDialog):
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
        with audioread.audio_open(self.filename) as ex:
            dur = int(ex.duration * 1000)
        s = Song(name=self.name_input.text(), duration=dur,
                     artist=self.artist_input.text(),
                 record=self.record_input.text(), file_path=self.filename)
        session.add(s)
        session.commit()
        self.close()

    def get_file(self):
        # fd = QFileDialog(self)
        # fd.exec()
        file_path = QFileDialog.getOpenFileName(self, 'Open file', '~/', "Audio files (*.mp3 *.wav)")
        # print(filename)
        self.file_label.setText(file_path[0].split('/')[-1])
        self.filename = file_path[0]
        self.warning_label.setText('')

class SelectSongDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('QT_windows/select_song.ui', self)
        self.buttonBox.accepted.connect(self.selected)

    def selected(self):
        form = SongForm(self)
        form.exec()


class SongView(QDialog):
    player = None
    playing = False
    started = False
    stop_position = 0
    def __init__(self, parent, player, duration):
        super().__init__(parent)
        uic.loadUi('QT_windows/song_view.ui', self)
        self.play_stop_button.clicked.connect(self.play_stop)
        self.playing = False
        self.player = player
        self.player.positionChanged.connect(self.position_changed)
        self.song_slider.valueChanged.connect(self.slider_moved)
        self.song_slider.setMaximum(duration)

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
        self.songs_list.addItems([e.name for e in session.query(Song).all()])
        self.songs_list.itemClicked.connect(self.show_song)

    def create_song_dialog(self):
        dialog = SongForm(self)
        dialog.exec()
        self.songs_list.clear()
        self.songs_list.addItems([e.name for e in session.query(Song).all()])

    def show_song(self, item):
        song = session.query(Song).filter(Song.name==item.text()).first()
        if not song:
            print(f"AAAAAAAA `{item.text()}`")
            return
        url = QtCore.QUrl.fromLocalFile(song.file_path)
        content = QtMultimedia.QMediaContent(url)
        player = QtMultimedia.QMediaPlayer()
        player.setMedia(content)
        dialog = SongView(self, player, song.duration)
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

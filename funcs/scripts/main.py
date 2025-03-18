import sys
from PyQt5 import QtWidgets
from funcs.interface import App
from tg_bot import bot


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

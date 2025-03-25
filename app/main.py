import sys
from PyQt5 import QtWidgets
from app.interface import App


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

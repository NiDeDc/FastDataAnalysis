from Ui.WaitingWindow import Ui_window
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt


class WaitingControl(QtWidgets.QWidget, Ui_window):
    def __init__(self):
        super(WaitingControl, self).__init__()
        self.setupUi(self)
        self.setFixedSize(500, 550)
        self.movie = QMovie('./image/wait.gif')
        self.movie.setScaledSize(QSize(500, 500))
        # self.label_wait = QtWidgets.QLabel(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setScaledContents(True)
        self.label.setMovie(self.movie)
        self.movie.start()

        # self.setFixedSize(200, 150)
        # background = QtWidgets.QFrame(self)
        # background.setStyleSheet("background-color:#fff;border-radius:10px;")
        # background.setGeometry(0, 0, 200, 150)
        # label = QtWidgets.QLabel(background)
        # label.setGeometry(0, 0, 200, 150)
        # movie = QMovie("wait.gif")
        # movie.setScaledSize(QSize(200, 150))
        # label.setScaledContents(True)
        # label.setMovie(movie)
        # movie.start()

    def Show(self):
        self.show()

    def Close(self):
        self.close()


import enum

from PyQt5.QtWidgets import *
from PyQt5 import uic
from pytube import Playlist, YouTube, Stream
from pytube.exceptions import VideoUnavailable, PytubeError


class UI_Index(enum.Enum):
    Home_Window = 0
    YoutubeDownloader_Window = 1
    Editor_Window = 2


class Home_Window(QMainWindow):
    def __init__(self):
        super(Home_Window, self).__init__()
        uic.loadUi("Home_Window.ui", self)
        self.YTdown_push.clicked.connect(self.YoutubeDownloader_clicker)
        self.Editor_push.clicked.connect(self.Editor_clicker)
        self.Settings_push.clicked.connect(self.Settings_clicker)


class YoutubeDownloader_Window(QMainWindow):
    def __init__(self):
        super(YoutubeDownloader_Window, self).__init__()
        uic.loadUi("YoutubeDownloader_Window.ui", self)
        self.Home_push.clicked.connect(self.Home_clicker)
        self.Editor_push.clicked.connect(self.Editor_clicker)
        self.Settings_push.clicked.connect(self.Settings_clicker)
        self.DownloadNow_pushButton.clicked.connect(self.downloadnow)
        self.AddToQueue_pushButton.clicked.connect(self.addtoqueue)
        self.Video_radioButton.clicked.connect(self.video_or_audio)
        self.Audio_radioButton.clicked.connect(self.video_or_audio)

    def video_or_audio(self):
        if (self.Video_radioButton.isChecked() or self.Audio_radioButton.isChecked()):
            self.YoutubeURL_lineEdit.setEnabled(True)
            self.DownloadNow_pushButton.setEnabled(True)
            self.AddToQueue_pushButton.setEnabled(True)

    def addtoqueue(self):
        try:
            media = YouTube(self.YoutubeURL_lineEdit.text())
            self.DownProcesses_tableWidget.insertRow(self.DownProcesses_tableWidget.rowCount())
            # self.DownProcesses_tableWidget.setItem(self.DownProcesses_tableWidget.rowCount(), 1, media.thumbnail_url)
            self.DownProcesses_tableWidget.setItem(self.DownProcesses_tableWidget.currentRow(), 1,
                                                   QTableWidgetItem(media.channel_id))
            # self.DownProcesses_tableWidget.setItem(self.DownProcesses_tableWidget.rowCount(), 3, QTableWidgetItem(media.title))
            # self.DownProcesses_tableWidget.setItem(self.DownProcesses_tableWidget.rowCount(), 4, #PROGRESS)
        except PytubeError:
            message_except = QMessageBox()
            message_except.setText("Invalid URL, please try again.")
            message_except.exec()

        # playlist_url = self.YoutubeURL_lineEdit.text()
        # p = Playlist(playlist_url)
        # for url in p.video_urls:
        #     try:
        #         yt = YouTube(url)
        #     except VideoUnavailable:
        #         message = QMessageBox()
        #         message.setText("Invalid URL or media, please try again.")
        #         message.exec()
        #
        #     else:
        #         message_ok = QMessageBox()
        #         message_ok.setText("Test Worked")
        #         message_ok.exec()
        #         #yt.streams.first().download()

    def downloadnow(self):
        try:
            media = YouTube(self.YoutubeURL_lineEdit.text())
        except PytubeError:
            message_except = QMessageBox()
            message_except.setText("Invalid URL, please try again.")
            message_except.exec()
        else:
            message_ok = QMessageBox()
            message_ok.setText("Now downloading ...")
            message_ok.exec()


class Editor_Window(QMainWindow):
    def __init__(self):
        super(Editor_Window, self).__init__()
        uic.loadUi("Editor_Window.ui", self)
        self.Home_push.clicked.connect(self.Home_clicker)
        self.YTdown_push.clicked.connect(self.YoutubeDownloader_clicker)
        self.Settings_push.clicked.connect(self.Settings_clicker)


class Settings_Window(QMainWindow):
    def __init__(self):
        super(Settings_Window, self).__init__()
        uic.loadUi("Settings_Window.ui", self)
        self.Home_push.clicked.connect(self.Home_clicker)
        self.Editor_push.clicked.connect(self.Editor_clicker)
        self.YTdown_push.clicked.connect(self.YoutubeDownloader_clicker)

import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from pytube import Playlist, YouTube, Stream
from pytube.exceptions import VideoUnavailable, PytubeError


class Home_Window(QMainWindow):
    def __init__(self):
        super(Home_Window, self).__init__()
        uic.loadUi("Home_Window.ui", self)
        self.YTdown_push.clicked.connect(self.YoutubeDownloader_clicker)
        self.Editor_push.clicked.connect(self.Editor_clicker)
        self.Settings_push.clicked.connect(self.Settings_clicker)


    def YoutubeDownloader_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)# YTDOWNLOADER Window index is 1 in stack so we increment +1
    def Editor_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)
    def Settings_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() + 3)

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

    def Home_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def Editor_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def Settings_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() + 2)

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

    def YoutubeDownloader_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def Home_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def Settings_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Settings_Window(QMainWindow):
    def __init__(self):
        super(Settings_Window, self).__init__()
        uic.loadUi("Settings_Window.ui", self)
        self.Home_push.clicked.connect(self.Home_clicker)
        self.Editor_push.clicked.connect(self.Editor_clicker)
        self.YTdown_push.clicked.connect(self.YoutubeDownloader_clicker)

    def YoutubeDownloader_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def Editor_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def Home_clicker(self):
        widget.setCurrentIndex(widget.currentIndex() - 3)

# main
app = QApplication(sys.argv)
widget = QStackedWidget()
Homewindow = Home_Window()
YTDownloadWindow = YoutubeDownloader_Window()
EditorWindow = Editor_Window()
SettingsWindow = Settings_Window()
widget.addWidget(Homewindow)
widget.addWidget(YTDownloadWindow)
widget.addWidget(EditorWindow)
widget.addWidget(SettingsWindow)
widget.setFixedHeight(1000)
widget.setFixedWidth(1000)
widget.show()
app.exec()

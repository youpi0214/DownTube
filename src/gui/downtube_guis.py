import enum

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from pytube import Playlist, YouTube, Stream
from pytube.exceptions import VideoUnavailable, PytubeError

class UIsIndex(enum.Enum):
    HomeView = 0
    YoutubeDownloaderView = 1
    EditorView = 2
    AudioView = 3
    SettingsView = 4
    AboutView = 5
    HelpView = 6


class BaseView(QMainWindow):

    def __init__(self, p_height: int = 720, p_width: int = 1080):
        super(BaseView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/main_window.ui", self)
        self.setFixedWidth(p_width)
        self.setFixedHeight(p_height)
        self.container: QVBoxLayout
        self.rightMenuContainer: QStackedWidget = QStackedWidget()
        self.container.addWidget(self.rightMenuContainer)

        self.home_view_btn: QPushButton
        self.download_view_btn: QPushButton
        self.video_edit_view_btn: QPushButton
        self.audio_edit_view_btn: QPushButton
        self.settings_view_btn: QPushButton
        self.about_view_btn: QPushButton
        self.help_view_btn: QPushButton

        self.__addUIs()

    def __addUIs(self):
        self.rightMenuContainer.addWidget(HomeView())
        self.rightMenuContainer.addWidget(YoutubeDownloaderView())
        self.rightMenuContainer.addWidget(VideoEditorView())
        self.rightMenuContainer.addWidget(AudioEditorView())
        self.rightMenuContainer.addWidget(SettingsView())
        self.rightMenuContainer.addWidget(AboutView())
        self.rightMenuContainer.addWidget(HelpView())

    def switch_view(self):
        sender = self.sender()
        if sender == self.download_view_btn:
            self.rightMenuContainer.setCurrentIndex(0)
        if sender == self.home_view_btn:
            self.rightMenuContainer.setCurrentIndex(UIsIndex.HomeView.value)
        elif sender == self.download_view_btn:
            self.rightMenuContainer.setCurrentIndex(UIsIndex.YoutubeDownloaderView.value)
        elif sender == self.video_edit_view_btn:
            self.rightMenuContainer.setCurrentIndex(UIsIndex.EditorView.value)
        elif sender == self.audio_edit_view_btn:
            self.rightMenuContainer.setCurrentIndex(UIsIndex.AudioView.value)
        elif sender == self.settings_view_btn:
            self.rightMenuContainer.setCurrentIndex(UIsIndex.SettingsView.value)
        elif sender == self.about_view_btn:
            self.rightMenuContainer.setCurrentIndex(UIsIndex.AboutView.value)
        elif sender == self.help_view_btn:
            self.rightMenuContainer.setCurrentIndex(UIsIndex.HelpView.value)


class HomeView(QWidget):
    def __init__(self):
        super(HomeView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/home_view.ui", self)


class YoutubeDownloaderView(QWidget):
    def __init__(self):
        super(YoutubeDownloaderView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/downloader_view.ui", self)

        self.DownloadNow_pushButton.clicked.connect(self.download_now)
        self.AddToQueue_pushButton.clicked.connect(self.add_to_queue)
        self.Video_radioButton.clicked.connect(self.video_or_audio)
        self.Audio_radioButton.clicked.connect(self.video_or_audio)

    def video_or_audio(self):
        if self.Video_radioButton.isChecked() or self.Audio_radioButton.isChecked():
            self.YoutubeURL_lineEdit.setEnabled(True)
            self.DownloadNow_pushButton.setEnabled(True)
            self.AddToQueue_pushButton.setEnabled(True)

    def add_to_queue(self):
        try:
            url_validation_test = YouTube(self.YoutubeURL_lineEdit.text()) # Temporary line, we will have to call a function in backend that handles exceptions before downloading
            self.DownProcesses_tableWidget.insertRow(self.DownProcesses_tableWidget.rowCount())
            self.mediaDataInsertion(self.YoutubeURL_lineEdit.text(), self.DownProcesses_tableWidget.rowCount() - 1)
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

    def download_now(self):
        try:
            url_validation_test = YouTube(self.YoutubeURL_lineEdit.text()) # Temporary line, we will have to call a function in backend that handles exceptions before downloading
            self.DownProcesses_tableWidget.insertRow(0)
            self.mediaDataInsertion(self.YoutubeURL_lineEdit.text(), 0)

        except PytubeError:
            message_except = QMessageBox()
            message_except.setText("Invalid URL, please try again.")
            message_except.exec()

    def mediaDataInsertion(self, URL : str, current_row : int):
        media = YouTube(URL)
        thumbnail_qitem = QTableWidgetItem(media.thumbnail_url)
        author_qitem = QTableWidgetItem(media.author)
        title_qitem = QTableWidgetItem(media.title)
        #self.progressbar = QProgressBar(self)
        #progress_bar_qitem = QTableWidgetItem(self.progressbar)
        self.DownProcesses_tableWidget.setItem(current_row, 0,
                                               thumbnail_qitem)
        self.DownProcesses_tableWidget.setItem(current_row, 1,
                                               author_qitem)
        self.DownProcesses_tableWidget.setItem(current_row, 2,
                                               title_qitem)
        # self.DownProcesses_tableWidget.setItem(current_row, 3,
        #                                        progress_bar_qitem)


        thumbnail_qitem.setTextAlignment(QtCore.Qt.AlignCenter)
        author_qitem.setTextAlignment(QtCore.Qt.AlignCenter)
        title_qitem.setTextAlignment(QtCore.Qt.AlignCenter)




class VideoEditorView(QWidget):
    def __init__(self):
        super(VideoEditorView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/video_editor_view.ui", self)


class AudioEditorView(QWidget):
    def __init__(self):
        super(AudioEditorView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/audio_editor_view.ui", self)


class SettingsView(QWidget):
    def __init__(self):
        super(SettingsView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/settings_view.ui", self)


class AboutView(QWidget):
    def __init__(self):
        super(AboutView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/about_view.ui", self)


class HelpView(QWidget):
    def __init__(self):
        super(HelpView, self).__init__()
        uic.loadUi("C:/Users/Ziyad/PycharmProjects/DownTube/resources/gui/help_view.ui", self)

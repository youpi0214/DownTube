from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.uic.properties import QtCore
from pytube import YouTube
from pytube.exceptions import PytubeError
from utilities.general_utilities import relative_to_abs_path, does_path_exist

DOWNLOAD_PATH = 'download_path'
EDIT_LINE_VALUE = 'text_edit_value'
DEFAULT_PATH_CHECKED = 'default_path'


class DownloadOptionPopup(QDialog):

    def __init__(self):
        super(DownloadOptionPopup, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/popup_download_options.ui"), self)

        self.line_edit_path: QLineEdit
        self.default_path_checkBox: QCheckBox
        self.__init_state()

    @property
    def edit_path(self) -> QLineEdit:
        return self.line_edit_path

    @property
    def use_default_path(self) -> QCheckBox:
        return self.default_path_checkBox

    def __init_state(self):
        self.__state = {
            DOWNLOAD_PATH: {
                EDIT_LINE_VALUE: '',
                DEFAULT_PATH_CHECKED: True
            }
        }

    def cancel_option_change(self):
        self.line_edit_path.setText(self.__state[DOWNLOAD_PATH][EDIT_LINE_VALUE])
        self.default_path_checkBox.setChecked(self.__state[DOWNLOAD_PATH][DEFAULT_PATH_CHECKED])
        self.hide()

    def save_changes(self):
        """saves the configuration for futures downloads
        this will reset after the app is closed"""
        if (not self.default_path_checkBox.isChecked() and does_path_exist(self.line_edit_path.text())) \
                or self.default_path_checkBox.isChecked():
            self.__state[DOWNLOAD_PATH][EDIT_LINE_VALUE] = self.line_edit_path.text()
            self.__state[DOWNLOAD_PATH][DEFAULT_PATH_CHECKED] = self.default_path_checkBox.isChecked()
            self.hide()
        else:
            QMessageBox().critical(None, "ERROR",
                                   "PATH NOT FOUND!\nThe path is either Invalid or does not exist")


class YoutubeDownloaderView(QWidget):
    def __init__(self):
        super(YoutubeDownloaderView, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/downloader_view.ui"), self)
        self.dialog = DownloadOptionPopup()

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

    def download_options_popup(self):
        self.dialog.show()

    def download_now(self):
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

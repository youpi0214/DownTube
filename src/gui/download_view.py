import requests
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from pytube import YouTube
from pytube.exceptions import PytubeError
from utilities.general_utilities import relative_to_abs_path, does_path_exist
from utilities.video_utilities import SupportedAudioSampleRate, SupportedVideoResolution, SupportedVideoFPS

DOWNLOAD_PATH = 'download_path'
EDIT_LINE_VALUE = 'text_edit_value'
DEFAULT_PATH_CHECKED = 'default_path'
VIDEO_RES = 'video_res'
VIDEO_FPS = 'video_fps'
AUDIO_SAMPLERATE = 'audio_samplerate'
PROGRESSIVE = 'progressive'


class DownloadOptionPopup(QDialog):

    def __init__(self):
        super(DownloadOptionPopup, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/popup_download_options.ui"), self)

        self.line_edit_path: QLineEdit
        self.default_path_checkBox: QCheckBox
        self.video_res: QComboBox
        self.video_fps: QComboBox
        self.audio_sample_rate: QComboBox
        self.progressive_checkbox: QCheckBox
        self.__init_state()

    def on_default_checkBox(self):
        if self.default_path_checkBox.isChecked():
            self.line_edit_path.setDisabled(True)
        else:
            self.line_edit_path.setDisabled(False)

    @property
    def download_options(self) -> dict:
        """returns download options selected by the user"""
        return self.__state

    def __init_state(self):
        self.__state = {
            DOWNLOAD_PATH: {
                EDIT_LINE_VALUE: '',
                DEFAULT_PATH_CHECKED: True
            },
            # TODO (video resolution, fps and audio sample rate) use the default one set in the app settings (when
            #  the settings will be done)
            VIDEO_RES: SupportedVideoResolution.RES_720p.value,
            VIDEO_FPS: SupportedVideoFPS.FPS30.value,
            AUDIO_SAMPLERATE: SupportedAudioSampleRate.SAMP_R_128.value,
            PROGRESSIVE: False
        }

        self.default_path_checkBox.setChecked(True)
        for res in SupportedVideoResolution: self.video_res.addItem(res.value)
        for fps in SupportedVideoFPS: self.video_fps.addItem(fps.value)
        for sample_rate in SupportedAudioSampleRate: self.audio_sample_rate.addItem(sample_rate.value)
        self.progressive_checkbox.setChecked(False)

    def cancel_option_change(self):
        """cancels the current changes by reverting the options back to what they were before
        opening the dialog window"""
        self.line_edit_path.setText(self.__state[DOWNLOAD_PATH][EDIT_LINE_VALUE])
        self.default_path_checkBox.setChecked(self.__state[DOWNLOAD_PATH][DEFAULT_PATH_CHECKED])
        self.video_res.setCurrentText(self.__state[VIDEO_RES])
        self.video_fps.setCurrentText(self.__state[VIDEO_FPS])
        self.audio_sample_rate.setCurrentText(self.__state[AUDIO_SAMPLERATE])
        self.progressive_checkbox.setChecked(self.__state[PROGRESSIVE])
        self.hide()

    def save_changes(self):
        """saves the configuration for futures downloads
        this will reset after the app is closed"""

        if (not self.default_path_checkBox.isChecked() and does_path_exist(self.line_edit_path.text())) \
                or self.default_path_checkBox.isChecked():
            self.__state[DOWNLOAD_PATH][EDIT_LINE_VALUE] = self.line_edit_path.text()
            self.__state[DOWNLOAD_PATH][DEFAULT_PATH_CHECKED] = self.default_path_checkBox.isChecked()
            self.__state[VIDEO_RES] = self.video_res.currentText()
            self.__state[VIDEO_FPS] = self.video_fps.currentText()
            self.__state[AUDIO_SAMPLERATE] = self.audio_sample_rate.currentText()
            self.__state[PROGRESSIVE] = self.progressive_checkbox.isChecked()
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

    def download_options_popup(self):
        self.dialog.show()

    def video_or_audio(self):
        if self.Video_radioButton.isChecked() or self.Audio_radioButton.isChecked():
            self.YoutubeURL_lineEdit.setEnabled(True)
            self.DownloadNow_pushButton.setEnabled(True)
            self.AddToQueue_pushButton.setEnabled(True)

    def add_to_queue(self):
        try:
            # TODO backend call for data to display in the row goes here
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
            url_validation_test = YouTube(
                self.YoutubeURL_lineEdit.text())  # Temporary line, we will have to call a function in backend that handles exceptions before downloading
            self.DownProcesses_tableWidget.insertRow(0)
            self.mediaDataInsertion(self.YoutubeURL_lineEdit.text(), 0)

        except PytubeError:
            message_except = QMessageBox()
            message_except.setText("Invalid URL, please try again.")
            message_except.exec()

    def image_widget(self, URL: str):
        image = QtGui.QPixmap(URL)
        box2 = QHBoxLayout()
        mylabel = QLabel()
        mylabel.setPixmap(image)
        # mylabel.setGeometry(150, 80)
        box2.addWidget(mylabel)
        widget = QWidget()
        widget.setLayout(box2)
        return widget

    def mediaDataInsertion(self, URL: str, current_row: int):

        media = YouTube(URL)

        author_qitem = QTableWidgetItem(media.author)
        title_qitem = QTableWidgetItem(media.title)

        box = QHBoxLayout()  # On cree une box, et un autre widget. On etablie ensuite la taille du widget a celui de la box qui contient le progress bar
        box.addWidget(QProgressBar())
        w = QWidget()
        w.setLayout(box)

        thumbnail_data = QtGui.QImage()
        thumbnail_data.loadFromData(requests.get(media.thumbnail_url).content)
        thumbnail = self.image_widget(thumbnail_data)

        # download_button_image = self.image_widget("C:/Users/Ziyad/Desktop/DownTube_download_logo.png")

        self.DownProcesses_tableWidget.setCellWidget(current_row, 0, thumbnail)
        self.DownProcesses_tableWidget.setItem(current_row, 1,
                                               author_qitem)
        self.DownProcesses_tableWidget.setItem(current_row, 2,
                                               title_qitem)
        self.DownProcesses_tableWidget.setCellWidget(current_row, 3, w)

        self.DownProcesses_tableWidget.setCellWidget(current_row, 4, thumbnail)

        author_qitem.setTextAlignment(QtCore.Qt.AlignCenter)
        title_qitem.setTextAlignment(QtCore.Qt.AlignCenter)

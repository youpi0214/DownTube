from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from controllers.download_controller import DownloadController
from utilities.general_utilities import relative_to_abs_path, does_path_exist
from utilities.video_utilities import *


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


class DownProcessesTableRow:

    def __init__(self, p_current_row: int, p_thumbnail_file, p_author: str, p_title: str, p_progressbar: QProgressBar):
        self.current_row = p_current_row
        self.__image_widget(p_thumbnail_file)
        self.author_qitem: QTableWidgetItem = QTableWidgetItem(p_author)
        self.title_qitem: QTableWidgetItem = QTableWidgetItem(p_title)
        self.progressbar = p_progressbar  # TODO

        self.author_qitem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.title_qitem.setTextAlignment(QtCore.Qt.AlignCenter)

    def __image_widget(self, p_image_file: str):
        self.image: QWidget = QWidget()
        image_displayer = QLabel(self.image)
        image_displayer.setPixmap(QPixmap(p_image_file))
        image_displayer.setScaledContents(True)
        image_displayer.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def __progressbar(self, p_progressbar: QProgressBar):
        self.progressbar: QProgressBar = p_progressbar
        # TODO finish progressbar

    def __del__(self):
        """TODO destructor remove the listener on the progressbar"""
        pass

    def add_process_row_to_table(self, p_table_widget: QTableWidget):
        pass


class YoutubeDownloaderView(QWidget):
    def __init__(self, p_controller):
        super(YoutubeDownloaderView, self).__init__()
        self.download_controller: DownloadController = p_controller
        uic.loadUi(relative_to_abs_path("resources/gui/downloader_view.ui"), self)
        self.dialog = DownloadOptionPopup()

        self.youtubeURL_lineEdit: QLineEdit
        self.downloadNow_pushButton: QPushButton
        self.addToQueue_pushButton: QPushButton
        self.video_radioButton: QRadioButton
        self.audio_radioButton: QRadioButton
        self.downloadProcess_tableWidget: QTableWidget

    def download_options_popup(self):
        self.dialog.show()

    def enable_download_and_linkEdit(self):
        """enables the link editor, the download now button and add to queue button if and only if the user selected
        which type of media he wants to download"""
        if self.video_radioButton.isChecked() or self.audio_radioButton.isChecked():
            self.youtubeURL_lineEdit.setEnabled(True)
            self.downloadNow_pushButton.setEnabled(True)
            self.addToQueue_pushButton.setEnabled(True)

    def download_now(self):
        download_process_metadata = self.download_controller.add_downloadProcess_backend(
            self.youtubeURL_lineEdit.text())
        self.downloadProcess_tableWidget.insertRow(0)
        self.__add_downloadProcess_view(0)

    def add_to_queue(self):
        download_process_metadata = self.download_controller.add_downloadProcess_backend(
            self.youtubeURL_lineEdit.text())
        self.downloadProcess_tableWidget.insertRow(self.downloadProcess_tableWidget.rowCount())
        self.__add_downloadProcess_view(self.downloadProcess_tableWidget.rowCount() - 1)

    def __add_downloadProcess_view(self, p_current_row: int, p_thumbnail_file, p_author: str, p_title: str):
        process_row = DownProcessesTableRow(p_current_row, p_thumbnail_file, p_author, p_title, QProgressBar())
        process_row.add_process_row_to_table(self.downloadProcess_tableWidget)

    def delete_process_row(self):
        # TODO determine the process clicked on
        # TODO stop backend download
        # TODO delete process in backend
        # TODO lastly deleteprocess in view
        pass

# thumbnail_data = QImage()
# thumbnail_data.loadFromData(requests.get(media.thumbnail_url).content)
# thumbnail = self.image_widget(thumbnail_data)

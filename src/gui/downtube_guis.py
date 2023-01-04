import enum

from PyQt5.QtWidgets import *
from PyQt5 import uic

from gui.download_view import YoutubeDownloaderView
from utilities.general_utilities import relative_to_abs_path


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
        uic.loadUi("C:/Users/ouamb/Documents/Github/DownTube/resources/gui/main_window.ui", self)
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
        uic.loadUi(relative_to_abs_path("resources/gui/home_view.ui"), self)


class VideoEditorView(QWidget):
    def __init__(self):
        super(VideoEditorView, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/video_editor_view.ui"), self)


class AudioEditorView(QWidget):
    def __init__(self):
        super(AudioEditorView, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/audio_editor_view.ui"), self)


class SettingsView(QWidget):
    def __init__(self):
        super(SettingsView, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/settings_view.ui"), self)


class AboutView(QWidget):
    def __init__(self):
        super(AboutView, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/about_view.ui"), self)


class HelpView(QWidget):
    def __init__(self):
        super(HelpView, self).__init__()
        uic.loadUi(relative_to_abs_path("resources/gui/help_view.ui"), self)

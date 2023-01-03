import sys

from PyQt5.QtWidgets import *
from gui.downtube_guis import Editor_Window, Settings_Window, Home_Window, YoutubeDownloader_Window

if __name__ == '__main__':
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

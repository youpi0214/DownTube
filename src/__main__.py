import json
import os.path
import pathlib
import sys

from PyQt5.QtWidgets import *
from pytube import YouTube

import utilities.general_utilities
from gui.downtube_guis import ViewController


class Controller:

    def __init__(self):
        self.base_view = ViewController()

    def display_view(self):
        self.base_view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    controller.display_view()
    app.exec()

    # from yt_dlp import YoutubeDL
    #
    # URL = 'https://www.youtube.com/watch?v=r1Fx0tqK5Z4&ab_channel=SashaSloanVEVO'
    # ydl_opts = {}
    # with YoutubeDL(ydl_opts) as ydl:
    #     info = ydl.extract_info(URL, download=False)
    #
    #     # ℹ️ ydl.sanitize_info makes the info json-serializable
    #     print(json.dumps(ydl.sanitize_info(info)))

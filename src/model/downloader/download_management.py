import enum
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from pytube import YouTube
from pytube.cli import on_progress
from pytube.exceptions import RegexMatchError

from utilities import general_utilities
from utilities.general_utilities import does_path_exist
from utilities.video_utilities import *


# class Downloader(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.progress_bar = QtWidgets.QProgressBar(self)
#         self.progress_bar.setGeometry(30, 40, 200, 25)
#
#         self.download_button = QtWidgets.QPushButton("Download", self)
#         self.download_button.clicked.connect(self.download_video)
#         self.download_button.move(40, 80)
#
#     def download_video(self):
#         url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#         process = subprocess.Popen(["youtube-dl", "--no-progress", url],
#                                    stdout=subprocess.PIPE,
#                                    stderr=subprocess.PIPE)
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(lambda: self.update_progress(process))
#         timer.start(100)
#
#     def update_progress(self, process):
#         progress = process.stderr.readline().decode("utf-8").strip()
#         if "[download]" in progress:
#             fraction_complete = float(progress.split("%")[0].split("[download]")[-1].strip())
#             self.progress_bar.setValue(fraction_complete)

class DownloadState(enum.Enum):
    """List of possible states of a Download Process"""
    READY = 0
    DOWNLOADING = 1
    PAUSED = 2
    FINISHED = 3
    CANCELLED = 4
    FAILED = -1


class DownloadProcess():

    def __init__(self, p_link, p_download_selected_options: dict):
        if does_path_exist(p_download_selected_options[DOWNLOAD_PATH][EDIT_LINE_VALUE]):
            self.process = None
            self.filename = None
            self.link = p_link
            self.download_selected_options = p_download_selected_options
            self.state = DownloadState.READY
        else:
            raise TypeError("Invalid or Non-existing destination path")

    def start_download(self, p_resume: bool):
        """Attempts to download the video given the url and option picked by the user.
         if an option is not available, it automatically picks the closest option available (better or worse).


         Example: option 720p is not available for download, the program either downloads the 480p or 1080p resolution
         of the vid is available. throws an error if the video is not available/restricted"""

        try:
            title = general_utilities.slugify(value=self.title) + '.mp4'
            if self.process and self.process.poll() is not None:

                args = ["youtube-dl", "--no-continue", "--get-filename", self.link]
                if p_resume:
                    args.append("--continue")

                self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.filename = self.process.stdout.read().strip().decode()

                self.state = DownloadState.DOWNLOADING
        except TimeoutError:
            pass
        except Exception:
            pass

    def track_download_progress(self, stream=None, chunk=None, file_handle=None, remaining=None):
        pass

    def cancel_download(self):
        """this method cancels the download and also removes the downloaded data"""
        # TODO this one will be a tough one hahahaha downloading will need to be enhanced/rewrote to implement this
        if self.process and self.process.poll() is None:
            self.process.terminate()
            if self.filename:
                os.remove(self.filename)
            self.state = DownloadState.CANCELLED

    def resume_download(self):
        self.start_download(p_resume=True)

    def pause_download(self):
        # TODO this one will be a tough one downloading will need to be enhanced/rewrote to implement this
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.state = DownloadState.PAUSED


class DownloadProcessManager:

    def __init__(self):
        self.__download_processes_dict: dict = {}
        self.thread_pool_excecutor: ThreadPoolExecutor = ThreadPoolExecutor(
            10)  # TODO noumber of workers will set in the settings of the app

    def add_new_download_process(self, p_url: str, download_selected_options: dict):
        try:
            self.__download_processes_dict[p_url] = DownloadProcess(p_url, download_selected_options)
        except RegexMatchError:
            # TODO throw RegexMatchError again with a message specifying that the url is not a a valid youtube url
            pass



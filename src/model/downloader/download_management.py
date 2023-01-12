import enum
from concurrent.futures import ThreadPoolExecutor

from pytube import YouTube
from pytube.cli import on_progress
from pytube.exceptions import RegexMatchError

from utilities import general_utilities
from utilities.general_utilities import does_path_exist
from utilities.video_utilities import *


class DownloadState(enum.Enum):
    """List of possible states of a Download Process"""
    READY = 0
    DOWNLOADING = 1
    PAUSED = 2
    FINISHED = 3
    CANCELLED = 4
    FAILED = -1


class DownloadProcess(YouTube):

    def __init__(self, p_link, p_download_selected_options: dict):
        super(DownloadProcess, self).__init__(p_link, on_progress_callback=on_progress)
        if does_path_exist(p_download_selected_options[DOWNLOAD_PATH][EDIT_LINE_VALUE]):
            self.download_selected_options = p_download_selected_options
            self.state = DownloadState.READY
        else:
            raise TypeError("Invalid or Non-existing destination path")

    def start_download(self):
        """Attempts to download the video given the url and option picked by the user.
         if an option is not available, it automatically picks the closest option available (better or worse).


         Example: option 720p is not available for download, the program either downloads the 480p or 1080p resolution
         of the vid is available. throws an error if the video is not available/restricted"""

        try:
            title = general_utilities.slugify(value=self.title) + '.mp4'

            self.state = DownloadState.DOWNLOADING
        except TimeoutError:
            pass
        except Exception:
            pass

    def track_download_progress(self, stream=None, chunk=None, file_handle=None, remaining=None):
        pass

    def cancel_download(self):
        # TODO this one will be a tough one hahahaha downloading will need to be enhanced/rewrote to implement this
        pass

    def pause_download(self):
        # TODO this one will be a tough one downloading will need to be enhanced/rewrote to implement this
        pass


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

# exemple of progress tracker
# def progress_Check(stream=None, chunk=None, file_handle=None, remaining=None):
#
#     percent = file_size - remaining + 1000000
#
#     try:
#         # updates the progress bar
#         bar.update(round(percent / 1000000, 2))
#     except:
#         # progress bar dont reach 100% so a little trick to make it 100
#         bar.update(round(file_size / 1000000, 2))

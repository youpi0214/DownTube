import enum

from pytube import YouTube
from pytube.cli import on_progress

from utilities import general_utilities


class DownloadState(enum.Enum):
    """List of possible states of a Download Process"""
    READY = 0
    DOWNLOADING = 1
    PAUSED = 2
    FINISHED = 3
    CANCELLED = 4
    FAILED = -1


class DownloadProcess(YouTube):

    def __init__(self, p_link, **kwargs):
        super(DownloadProcess, self).__init__(p_link, on_progress_callback=on_progress)
        self.state = DownloadState.READY
        self.streams.first()
        param = kwargs

    def start_download(self):

        try:
            title = general_utilities.slugify(value=self.title) + '.mp4'
            self.streams.filter(file_extension='mp4').get_highest_resolution().download(skip_existing=False, timeout=5,
                                                                                        filename=title)
            self.state = DownloadState.DOWNLOADING
        except TimeoutError:
            pass
        except Exception:
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

from pytube import YouTube
from pytube.cli import on_progress
import unicodedata
import re


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class DownloadProcess(YouTube):

    def __init__(self, p_link, **kwargs):
        super(DownloadProcess, self).__init__(p_link, on_progress_callback=on_progress)
        self.streams.first()
        param = kwargs

    def start_download(self):
        title = slugify(value=self.title) + '.mp4'
        self.streams.filter(file_extension='mp4').get_highest_resolution().download(skip_existing=False, timeout=5,
                                                                                    filename=title)


if __name__ == '__main__':
    test = DownloadProcess('https://youtu.be/9bZkp7q19f0')
    test.start_download()

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

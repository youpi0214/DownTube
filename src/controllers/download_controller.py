from model.downloader.download_management import DownloadProcessManager


class DownloadController:

    def __init__(self):
        self.download_process_manager = DownloadProcessManager()
    def get_media_meta_data(self, p_url: str):
        pass

    def add_downloadProcess_backend(self, p_url: str) -> dict:
        """tries to add a download process and returns its metadata"""

        return {}

import sys
from io import StringIO
from logging import info, exception, error
from re import findall
from subprocess import run
from threading import Thread

import youtube_dl
from os.path import abspath, splitext
from os.path import exists, join
from persistqueue import SQLiteAckQueue
from send2trash import send2trash
from utility.os_interface import get_cwd, change_dir


class FileDownload(StringIO):
    def __init__(self, ffmpeg_path, url, video_command, downloader):
        StringIO.__init__(self)
        # Download the url
        self._current_url = url
        self._downloader = downloader
        self._size = None
        self._current_file = []
        """
        Enter processing one queue item
        """
        # Redirect stdout to custom function
        old_stdout = sys.stdout
        sys.stdout = self
        # Change cwd to file output directory
        self._os_dir = get_cwd()
        change_dir(self._downloader.download_path)

        with self:
            try:
                youtube_dl.main([url, '--no-check-certificate', '--no-playlist', '-f %sbestaudio' % video_command])
                # , '-U'
            except SystemExit as e:
                info(e)

            # Join audio and video
            if video_command:
                name, _ = splitext(self._current_file[-1])
                self._current_file.append(name[:-5] + '.mp4')
                run(ffmpeg_path +
                    ' -i "%s" -i "%s" -c:v copy -c:a copy  -strict experimental -map 0:v:0 -map 1:a:0 "%s"' %
                    tuple(self._current_file), shell=False)
                # Delete audio and video files
                send2trash(self._current_file[0])
                send2trash(self._current_file[1])
        """
        Exit queue item processing
        """
        # Reset stdout to normal
        sys.stdout = old_stdout
        # Reset cwd to normal
        change_dir(self._os_dir)
        info("Download: DONE")

    def write(self, string):
        """
        Overwrite StringIO write().
        Parses youtube-dl Stdout output (https://stackoverflow.com/a/19345047)
        :param string: Stdout string
        :return: StringIO return value
        """
        # TODO read err and out simultaneously

        line = string.strip()
        info(line)

        progress = findall('(\d*\.?\d%)', line)
        if progress:
            self._downloader.set_download_progress(progress[-1])

            # Get file size
            if not self._size:
                size = findall('of\s([^\s]+)', line)
                if len(size) == 1:
                    self._size = size[0]
                    self._downloader.set_download_size(self._size)

        elif line.startswith('[download] Destination: '):
            file_name = line.replace('[download] Destination: ', "")
            self._current_file.append(join(self._downloader.download_path, file_name))
            self._downloader.set_download_title(file_name, self._current_url)

        elif line.endswith('has already been downloaded'):
            file_name = line.replace(' has already been downloaded', "").replace('[download] ', '')
            self._current_file.append(join(self._downloader.download_path, file_name))
            self._downloader.set_download_title(file_name, self._current_url)
        # No else: irrelevant line

        return super().write(string)

    @property
    def success(self):
        return self._current_file and exists(self._current_file[-1])


class Downloader(Thread):
    _Controller = None
    _download_queue = None
    _active = True
    _counter = -1

    def __init__(self, controller, download_path, queue_path, SelectionVideo, ffmpeg_path):
        Thread.__init__(self)
        self._Controller = controller
        self.daemon = True  # Stop thread, when program is closed
        self._ffmpeg_path = ffmpeg_path
        self.download_path = download_path
        queue_path = abspath(queue_path)
        self._download_queue = SQLiteAckQueue(path=queue_path, multithreading=True, auto_commit=True)
        self.get_command = {SelectionVideo.NO_VIDEO.value: '', SelectionVideo.VIDEO.value: 'bestvideo+'}

    # TODO test directory delete
    # TODO handle playlists
    def run(self) -> None:
        """
        Overwrite Thread.run().
        If queue is not empty, download the first element
        """
        try:
            while self._active:
                info('DOWNLOAD QUEUE SIZE %s' % self._download_queue.size)
                item = self._download_queue.get()
                url, video_command = item

                info('DOWNLOAD: %s' % url)
                self._counter += 1
                if video_command in self.get_command:  # TODO REMOVE THIS
                    video_command = self.get_command[video_command]  # TODO REMOVE THIS

                current_file = FileDownload(self._ffmpeg_path, url, video_command, self)
                # Save queue
                if current_file.success:
                    self._download_queue.ack(item)
                    info('DOWNLOAD QUEUE saved after download %s' % url)
                del current_file
        except Exception as e:
            exception(e)
            pass

    def download(self, url: str, video_choice: str) -> None:
        """
        Add new url to the queue
        :param url: Url string
        :param video_choice: Url string
        """

        url = url.strip()
        video_choice = self.get_command[video_choice]
        self._download_queue.put((url, video_choice))

        info('Added to queue: %s' % url)

    # +++ CONTROLLER +++

    def set_download_progress(self, percent):
        self._Controller.set_download_progress(self._counter, percent)

    def set_download_title(self, title, url):
        self._Controller.set_download_title(self._counter, title, url)

    def set_download_size(self, size):
        self._Controller.set_download_size(self._counter, size)

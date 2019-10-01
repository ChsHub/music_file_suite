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
from utility.os_interface import get_cwd, change_dir


class Downloader(Thread, StringIO):
    _Controller = None
    _download_queue = None
    _active = True
    _current_url = None
    _size = None
    _current_file = []

    def __init__(self, controller, download_path, queue_path, SelectionVideo, ffmpeg_path):
        Thread.__init__(self)
        StringIO.__init__(self)
        self._Controller = controller
        self._counter = -1
        self.daemon = True  # Stop thread, when program is closed
        self._ffmpeg_path = ffmpeg_path

        self._download_path = download_path
        queue_path = abspath(queue_path)
        self._download_queue = SQLiteAckQueue(path=queue_path, multithreading=True, auto_commit=True)
        self.get_video = {SelectionVideo.NO_VIDEO.value: '', SelectionVideo.VIDEO.value: 'bestvideo+'}

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
                url, video_choice = item
                error('DOWNLOAD: %s' % url)

                # Download the url
                self._current_url = url
                with self:
                    try:
                        self._counter += 1
                        youtube_dl.main([url, '--no-check-certificate', '--no-playlist',
                                         '-f %sbestaudio' % self.get_video[video_choice]])  # , '-U'
                    except SystemExit as e:
                        info(e)

                    # Join audio and video
                    if self.get_video[video_choice]:
                        name, ext = splitext(self._current_file[-1])
                        self._current_file.append(name[:-5] + '.mp4')
                        run(self._ffmpeg_path + ' -i "%s" -i "%s" -c:v copy -c:a copy  -strict experimental -map 0:v:0 -map 1:a:0 "%s"' % tuple(self._current_file))

                # Save queue
                if self._current_file and exists(self._current_file[-1]):
                    self._download_queue.ack(item)
                    info('DOWNLOAD QUEUE saved after download %s' % url)

                # Reset file name
                self._current_file = []
                self._size = None # TODO put this in extra class


        except Exception as e:
            exception(e)

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
            self._set_download_progress(progress[-1])

            # Get file size
            if not self._size:
                size = findall('of\s([^\s]+)', line)
                if len(size) == 1:
                    self._size = size[0]
                    self.set_download_size(self._size)

        elif line.startswith('[download] Destination: '):
            file_name = line.replace('[download] Destination: ', "")
            self._current_file.append(join(self._download_path, file_name))
            self._set_download_title(file_name, self._current_url)

        elif line.endswith('has already been downloaded'):
            file_name = line.replace(' has already been downloaded', "").replace('[download] ', '')
            self._current_file.append(join(self._download_path, file_name))
            self._set_download_title(file_name, self._current_url)
        # No else: irrelevant line

        return super().write(string)

    def __enter__(self):
        '''
        Enter processing one queue item
        :return:
        '''
        info('DOWNLOAD: %s' % self._current_url)
        # Change cwd to file output directory
        self._os_dir = get_cwd()
        change_dir(self._download_path)
        # Redirect stdout to custom function
        self._old_stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Exit queue item processing
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        '''
        info("Download: DONE")
        # Reset stdout to normal
        sys.stdout = self._old_stdout
        # Reset cwd to normal
        change_dir(self._os_dir)

    def download(self, url: str, video_choice: str) -> None:
        """
        Put new url into the queue
        :param url: Url string
        """

        url = url.strip()
        self._download_queue.put((url, video_choice))

        info('Added to queue: %s' % url)

    def _set_download_progress(self, percent):
        self._Controller.set_download_progress(self._counter, percent)

    def _set_download_title(self, title, url):
        self._Controller.set_download_title(self._counter, title, url)

    def set_download_size(self, size):
        self._Controller.set_download_size(self._counter, size)

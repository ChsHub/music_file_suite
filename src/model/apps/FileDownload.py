import sys
from io import StringIO
from logging import info
from os.path import exists, join, split, splitext
from re import findall
from subprocess import run
from time import sleep

import youtube_dl
from send2trash import send2trash


class FileDownload(StringIO):
    def __init__(self, ffmpeg_path, url, video_command, downloader):
        StringIO.__init__(self)
        # Download the url
        self._current_url = url
        self._downloader = downloader
        self._size = None
        self._current_file = []
        self._write_strategy = self._write_file_name
        """
        Enter processing one queue item
        """
        # Redirect stdout to custom function
        old_stdout = sys.stdout
        sys.stdout = self

        with self:
            try:
                youtube_dl.main([url, '--no-check-certificate', '--no-playlist', '--rm-cache-dir',
                                 '-f', '%sbestaudio' % video_command,
                                 '-o', ('%s' % self._downloader.download_path) + '/%(title)s.%(ext)s'])
            except SystemExit as e:
                info(e)

            # Join audio and video
            if video_command and self._current_file:
                name, _ = splitext(self._current_file[-1])
                self._current_file.append(name[:-5] + '.mp4')
                run(ffmpeg_path +
                    ' -i "%s" -i "%s" -c:v copy -c:a copy  -strict experimental -map 0:v:0 -map 1:a:0 "%s"' %
                    tuple(self._current_file), shell=False, cwd=self._downloader.download_path)
                # Delete audio and video files
                while exists(self._current_file[0]) or exists(self._current_file[1]):
                    send2trash(self._current_file[0])
                    send2trash(self._current_file[1])
                    sleep(1)
        """
        Exit queue item processing
        """
        # Reset stdout to normal
        sys.stdout = old_stdout
        info("Download: DONE")

    def _write_file_name(self, line) -> None:
        """
        First phase of youtube download: Read file name from line
        :param line: Input line
        """
        file_name = findall(r'(?:\[download\] Destination: (.+))|(?:\[download\] (.+) has already been downloaded)', line)
        if file_name:
            file_name = list(*file_name)
            file_name = ''.join(file_name).replace('/', '\\')

            # If file name is found set current file
            self._current_file.append(join(self._downloader.download_path, file_name))
            self._downloader.set_download_title(split(file_name)[-1], self._current_url)
            # Set strategy for next phase
            self._write_strategy = self._write_size

    def _write_progress(self, line: str) -> None:
        """
        Third phase of youtube download: Read progress in %
        :param line: Input line
        """
        progress = findall(r'(\d*\.?\d%)', line)
        if progress:
            progress = progress[-1]
            self._downloader.set_download_progress(progress)
            if progress == '100%':
                # Reset strategy
                self._write_strategy = self._write_file_name

    def _write_size(self, line: str) -> None:
        """
        Third phase of youtube download: Read file size
        :param line: Input line
        """
        size = findall(r'of\s([^\s]+)', line)
        if len(size) == 1:
            self._size = size[0]
            self._downloader.set_download_size(self._size)
            # Set strategy for next phase
            self._write_strategy = self._write_progress
            self._write_progress(line)

    def write(self, string):
        """
        Overwrite StringIO write().
        Parses youtube-dl Stdout output (https://stackoverflow.com/a/19345047)
        :param string: Stdout string
        :return: StringIO return value
        """
        line = string.strip()
        info(line)
        self._write_strategy(line)
        return super().write(string)

    @property
    def success(self):
        return self._current_file and exists(self._current_file[-1])

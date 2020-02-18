import sys
from io import StringIO
from logging import info
from os import chdir, getcwd
from os.path import exists, join
from os.path import splitext
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
        """
        Enter processing one queue item
        """
        # Redirect stdout to custom function
        old_stdout = sys.stdout
        sys.stdout = self
        # Change cwd to file output directory
        self._os_dir = getcwd()
        chdir(self._downloader.download_path)

        with self:
            try:
                youtube_dl.main([url, '--no-check-certificate', '--no-playlist', '-f %sbestaudio' % video_command])
                # , '-U'
            except SystemExit as e:
                info(e)

            # Join audio and video
            if video_command and self._current_file:
                name, _ = splitext(self._current_file[-1])
                self._current_file.append(name[:-5] + '.mp4')
                run(ffmpeg_path +
                    ' -i "%s" -i "%s" -c:v copy -c:a copy  -strict experimental -map 0:v:0 -map 1:a:0 "%s"' %
                    tuple(self._current_file), shell=False)
                # Delete audio and video files
                self._current_file[0] = self._current_file[0].replace('/', '\\')
                self._current_file[1] = self._current_file[1].replace('/', '\\')
                while exists(self._current_file[0]) or exists(self._current_file[1]):
                    send2trash(self._current_file[0])
                    send2trash(self._current_file[1])
                    sleep(1)
        """
        Exit queue item processing
        """
        # Reset stdout to normal
        sys.stdout = old_stdout
        # Reset cwd to normal
        chdir(self._os_dir)
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

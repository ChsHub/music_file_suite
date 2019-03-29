# -*- coding: utf8 -*-

from logging import info
from os.path import join
from subprocess import getoutput, run
from threading import BoundedSemaphore

from utility.os_interface import exists, make_directory
from utility.utilities import replace_file_type

from src.resource.paths import commands, input_command
from src.resource.texts import SelectionCodecs
from src.resource.texts import convert_directory


class Converter:
    def __init__(self, controller):
        self._jobs = []
        self._convert_sem = BoundedSemaphore(value=1)
        self._controller = controller
        self._resolve = {'vorbis': 'ogg', 'aac': 'm4a', 'mp3': 'mp3', 'opus': 'opus'}
        self._extension = {SelectionCodecs.EXTRACT:self._get_file_extension,
                           SelectionCodecs.MP3:lambda x, y: 'mp3',
                           SelectionCodecs.OPUS:lambda x, y: 'opus'}

    def add_job(self, path, files):
        with self._convert_sem:
            self._jobs.append((path, files))
        for file in files:
            self._controller.add_convert_line([file, "0%"])

    def start_convert(self, selection):
        info(selection)
        # Get strategy
        strategy = SelectionCodecs(selection)

        # copy for thread safety
        with self._convert_sem:
            jobs = list(self._jobs)

        # Receive command based on strategy
        command = commands[strategy]
        i = 0
        for path, files in jobs:

            make_directory(join(path, convert_directory))
            info("Convert: " + str(len(files)) + " files")

            for file in files:
                file_path = join(path, file)

                # Receive new file extension based on strategy
                extension = self._extension[strategy](file_path, i)
                output_file = self._get_output_file_path(extension, file_path)

                # If file already exists do nothing
                if exists(output_file):
                    self._controller.set_convert_progress(i, "FILE ALREADY EXISTS")
                # Else convert
                elif extension:
                    run(command.replace("input", file_path).replace("output", output_file))
                    self._controller.set_convert_progress(i, "100%")
                i += 1
        info("Convert: DONE")

    # +++ CONVERT STRATEGIES +++
    # TODO convert to temp path
    @staticmethod
    def _get_output_file_path(new_extension, file_path):
        file_path = file_path.split("/")
        file_path[-1] = replace_file_type(file_path[-1], new_extension)
        file_path.insert(-1, convert_directory)
        return join(*file_path)

    def _get_audio_codec(self, file_path:str) -> str:
        """
        Get codec via probe
        :param file_path: Input file location
        :return: Codec
        """
        command = input_command.replace("input", file_path)
        info("PROBING: " + command)
        audio_codec = getoutput(command)
        info("AUDIO CODEC: " + audio_codec)

        return audio_codec.strip()

    def _get_file_extension(self, file_path:str, i:int) -> (str, str):
        """
        Strategy for extracting original codec
        :param file_path: Input video file
        :param i: Index
        :return: New file extension, if codec is supported or empty string
        """
        # Get audio codec and look up, the file extension
        audio_codec = self._get_audio_codec(file_path)
        if audio_codec in self._resolve:
            return self._resolve[audio_codec]
        else:
            self._controller.set_convert_progress(i, "TYPE NOT FOUND")
            return ''


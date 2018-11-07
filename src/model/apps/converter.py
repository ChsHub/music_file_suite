# -*- coding: utf8 -*-

from logging import info
from subprocess import getoutput, run
from threading import BoundedSemaphore

from utility.os_interface import exists, make_directory
from utility.path_str import get_full_path
from utility.utilities import replace_file_type

from src.resource.paths import command_extract, input_command, command_best_mp3, command_best_opus
from src.resource.texts import SelectionCodecs
from src.resource.texts import convert_directory


class Converter:
    def __init__(self, controller):
        self._jobs = []
        self._convert_sem = BoundedSemaphore(value=1)
        self._controller = controller
        self._convert_file = {SelectionCodecs.EXTRACT: self._strategy_extract,
                              SelectionCodecs.MP3: self._strategy_high_mp3,
                              SelectionCodecs.OPUS: self._strategy_high_opus}
        self._resolve = {'vorbis': 'ogg', 'aac': 'm4a', 'mp3': 'mp3', 'opus': 'opus'}

    def add_job(self, path, files):
        with self._convert_sem:
            self._jobs.append((path, files))
        for file in files:
            self._controller.add_convert_line([file, "0%"])

    def start_convert(self, selection):
        info(selection)
        strategy = SelectionCodecs(selection)

        # TODO Refactor converter
        # TODO remove files from job list
        # 1 convert into temp
        # 2 make dir
        # 3 copy to dir

        # copy for thread safety
        with self._convert_sem:
            jobs = list(self._jobs)

        i = 0
        for path, files in jobs:

            make_directory(get_full_path(path, convert_directory))
            info("Convert: " + str(len(files)) + " files")

            for file in files:
                file_path = get_full_path(path, file)
                command, extension = self._convert_file[strategy](file_path, i)

                output_file = self._get_output_file_path(extension, file_path)
                if exists(output_file):
                    self._controller.set_convert_progress(i, "FILE ALREADY EXISTS")

                elif command:
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
        return get_full_path(*file_path)

    def _get_audio_codec(self, file_path):

        # get codec with probe
        command = input_command.replace("input", file_path)
        info("PROBING: " + command)

        audio_codec = getoutput(command)
        info("AUDIO CODEC: " + audio_codec)

        return audio_codec.strip()

    def _strategy_extract(self, file_path, i):

        audio_codec = self._get_audio_codec(file_path)
        if audio_codec in self._resolve:
            return command_extract, self._resolve[audio_codec]
        else:
            self._controller.set_convert_progress(i, "TYPE NOT FOUND")
            return '', ''

    def _strategy_high_mp3(self, file_path, i):
        return command_best_mp3, "mp3"

    def _strategy_high_opus(self, file_path, i):
        return command_best_opus, "opus"

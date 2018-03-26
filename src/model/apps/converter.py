# -*- coding: utf8 -*-

from logging import error, info
from re import sub
from subprocess import getoutput, Popen
from threading import BoundedSemaphore
# TODO TEST for UTF-8 safety
from utility.encoding import decode
from utility.os_interface import exists, get_cwd, make_directory, change_dir, get_file_list
from utility.path_str import get_full_path
from src.resource.texts import convert_directory
from src.resource.paths import command_extract, input_command, command_best_mp3, command_best_opus
from src.resource.texts import SelectionCodecs


class Converter:
    _jobs = []
    _controller = None
    _convert_file = None

    def __init__(self, controller):
        self._convert_sem = BoundedSemaphore(value=1)
        self._controller = controller

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

        if strategy == SelectionCodecs.EXTRACT:
            _convert_file = self._strategy_extract
        elif strategy == SelectionCodecs.MP3:
            _convert_file = self._strategy_high_mp3
        elif strategy == SelectionCodecs.OPUS:
            _convert_file = self._strategy_high_opus
        else:
            error("WRONG CODEC")
            return

        # copy for thread safety
        with self._convert_sem:
            jobs = list(self._jobs)

        i = 0
        for path, files in jobs:
            for file in files:
                path_to_convert_dir = "/".join([path, convert_directory])
                make_directory(path_to_convert_dir)
                file_path = get_full_path(path, file)
                info("Convert: " + str(len(files)) + " files")
                if _convert_file(file_path, "TODO TEMP PATH", path_to_convert_dir):
                    self._controller.set_convert_progress(i, "100%")
                else:
                    self._controller.set_convert_progress(i, "ERROR")
                i += 1

        info("Convert: DONE")

    # +++ CONVERT STRATEGIES +++
    # TODO convert to temp path
    # Return true, if successful otherwise false
    def _strategy_extract(self, file_path, temp_path, path_to_convert_dir):

        file_extension = self.get_file_extension(file_path)

        if file_extension:
            info("FOUND TYPE: " + file_extension)
            output_f = self._get_output_file_path(path_to_convert_dir, file_extension, file_path)

            if not exists(output_f):
                Popen(command_extract.replace("input", file_path).replace("output", output_f),
                      stdout=None, stderr=None, shell=False)
                return True
            else:
                info("FILE ALREADY EXISTS: " + file_path)
        else:
            error("TYPE NOT FOUND")
        return False

    @staticmethod
    def get_file_extension(file_path):

        # get codec with probe
        audio_codec = getoutput(input_command.replace("input", file_path))
        audio_codec = audio_codec.replace("\r", "").replace("\n", "")
        info("AUDIO CODEC: " + audio_codec)
        resolve = {'vorbis': 'ogg', 'aac': 'm4a', 'mp3': 'mp3'}

        if audio_codec in resolve.keys():
            return resolve[audio_codec]

        print("CODEC NOT SUPPORTED" + audio_codec)
        return False

    @staticmethod
    def _get_output_file_path(path_to_convert_dir, new_extension, file_path):
        result = sub(r'[^.]*$', new_extension, file_path)  # replace extension
        result = result.split("/")[-1]  # remove old path
        result = get_full_path(path_to_convert_dir, result)  # new path
        return result

    def _strategy_high_mp3(self, file_path, temp_path, path_to_convert_dir):

        output_f = self._get_output_file_path(path_to_convert_dir, "mp3", file_path)

        if not exists(output_f):
            Popen(command_best_mp3.replace("input", file_path).replace("output", output_f),
                  stdout=None, stderr=None, shell=False)
            return True
        else:
            info("FILE ALREADY EXISTS: " + file_path)

        return False

    def _strategy_high_opus(self, file_path, temp_path, path_to_convert_dir):

        output_f = self._get_output_file_path(path_to_convert_dir, "opus", file_path)

        if not exists(output_f):
            Popen(command_best_opus.replace("input", file_path).replace("output", output_f),
                  stdout=None, stderr=None, shell=False)
            return True
        else:
            info("FILE ALREADY EXISTS: " + file_path)

        return False

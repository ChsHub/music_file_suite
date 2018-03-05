# -*- coding: utf8 -*-
# import ffmpeg   todo

from logging import error, info
from re import sub
from subprocess import getoutput, Popen
from threading import BoundedSemaphore

from utility.encoding import decode
from utility.os_interface import exists, get_cwd, make_directory, change_dir, get_file_list
from utility.path_str import get_full_path
from resource.texts import convert_directory
from resource.paths import converter_command, input_command
from resource.texts import SelectionCodecs


class Converter:
    _jobs = []
    _controller = None
    _convert_file = None

    def __init__(self, controller):
        self._convert_sem = BoundedSemaphore(value=1)
        self._controller = controller

    def consume_element(self, path, files):
        with self._convert_sem:
            self._jobs.append((path, files))
        for file in files:
            self._controller.add_convert_line([file, "0%"])

    def start_convert(self, selection):
        info(selection)
        strategy = SelectionCodecs(selection)

        # TODO
        # 1 convert into temp
        # 2 make dir
        # 3 copy to dir

        if strategy == SelectionCodecs.EXTRACT:
            _convert_file = self._strategy_extract
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
                info("Convert: " + str(len(files)) + " files")

                if _convert_file(path, file, "TODO TEMP PATH", path_to_convert_dir):
                    self._controller.set_convert_progress(i, "100%")
                else:
                    self._controller.set_convert_progress(i, "ERROR")
                i += 1

        info("Convert: DONE")

    # +++ CONVERT STRATEGIES +++
    # Return true, if successful otherwise false
    def _strategy_extract(self, path, input_f, temp_path, path_to_convert_dir):

        input_f = get_full_path(path, input_f)
        # get codec with probe
        print("INPUT: " + input_f)

        # stream = ffmpeg.input(input_f)
        # stream = ffmpeg.output(stream, filename="o.mp3")
        # audio_codec = ffmpeg.run(stream)
        print(input_command.replace("input", input_f))
        audio_codec = getoutput(input_command.replace("input", input_f))

        file_extension = self.get_file_extension(audio_codec)

        if file_extension:
            info("FOUND TYPE: " + file_extension)
            output_f = sub(r'[^.]*$', file_extension, input_f)  # replace extension
            output_f = output_f.split("/")[-1]  # remove old path
            output_f = get_full_path(path_to_convert_dir, output_f)  # new path

            if not exists(output_f):
                Popen(converter_command.replace("input", input_f).replace("output", output_f),
                      stdout=None, stderr=None, shell=False)
                return True
            else:
                info("FILE ALREADY EXISTS: " + input_f)
        else:
            error("TYPE NOT FOUND")
        return False

    @staticmethod
    def get_file_extension(codec):

        codec = codec.replace("\r", "").replace("\n", "")
        info("AUDIO CODEC: " + codec)
        resolve = {'vorbis': 'ogg', 'aac': 'm4a', 'mp3': 'mp3'}

        if codec in resolve.keys():
            return resolve[codec]

        print("CODEC NOT SUPPORTED" + codec)
        return False

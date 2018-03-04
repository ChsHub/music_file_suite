# -*- coding: utf8 -*-
import ffmpeg # todo

from logging import error, info
from re import sub
from subprocess import call, getoutput, check_call
from threading import BoundedSemaphore

from utility.encoding import decode
from utility.os_interface import exists, get_cwd, make_directory, change_dir, get_file_list
from utility.path_str import get_full_path

from paths import converter_command, input_command


class Converter:
    def __init__(self):


        self.convert_sem = BoundedSemaphore(value=1)

    def get_file_extension(self, codec):

        codec = codec.replace("\r", "").replace("\n", "")
        print(codec)
        resolve = {'vorbis': 'ogg', 'aac': 'm4a', 'mp3': 'mp3'}

        if codec in resolve.keys():
            return resolve[codec]

        print("CODEC NOT SUPPORTED" + codec)
        return False

    def consume_element(self, path):

        with self.convert_sem:

            os_dir = get_cwd()
            path_to_convert_dir = get_full_path(path, "CONVERTED")

            make_directory(path_to_convert_dir)
            change_dir(path_to_convert_dir)
            files = get_file_list(path)

            info("Convert: " + str(len(files)) + " files")

            for input_f in files:
                input_f = get_full_path(path, input_f)
                # get codec with probe
                print("INPUT: " + input_f)

                #stream = ffmpeg.input(input_f)
                #stream = ffmpeg.output(stream, filename="o.mp3")
                #audio_codec = ffmpeg.run(stream)
                print(input_command.replace("input", input_f))
                audio_codec = getoutput(input_command.replace("input", input_f))#, shell=True)

                file_extension = self.get_file_extension(audio_codec)

                if file_extension:
                    print(file_extension)
                    output_f = sub(r'[^.]*$', file_extension, input_f)  # replace extension
                    output_f = output_f.split("/")[-1]  # remove old path
                    output_f = get_full_path(path_to_convert_dir, output_f)  # new path

                    if not exists(output_f):
                        call(converter_command.replace("input", input_f).replace("output", output_f),
                             stdout=None, stderr=None, shell=False)
                    else:
                        error("Convert: " + input_f)

            change_dir(os_dir)
            info("Convert: DONE")

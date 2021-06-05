from concurrent.futures.thread import ThreadPoolExecutor
from logging import info
from os import mkdir, cpu_count
from os.path import join, split, splitext, exists
from subprocess import getoutput, Popen
from threading import BoundedSemaphore
# TODO color GUI red on fail
from timerpy import Timer

from src.abstract.abstract_list_model import AbstractListModel


class Converter(AbstractListModel):
    def __init__(self, controller, texts, SelectionCodecs, ffmpeg_path):
        AbstractListModel.__init__(self, controller)
        self._convert_sem = BoundedSemaphore(value=1)
        self._zero_time = '00:00:00.0'
        self.convert_directory = texts['convert_directory']
        self._resolve = {'vorbis': 'ogg', 'aac': 'm4a', 'mp3': 'mp3', 'opus': 'opus'}
        self._extension = {SelectionCodecs.EXTRACT.value: self._get_file_extension,
                           SelectionCodecs.MP3.value: lambda x, y: 'mp3',
                           SelectionCodecs.OPUS.value: lambda x, y: 'opus',
                           SelectionCodecs.FLAC.value: lambda x, y: 'flac'}
        self._commands = self._get_convert_command(texts, SelectionCodecs, ffmpeg_path)
        self._input_command = self._get_input_command(texts)

        self._jobs = []

    def _get_input_command(self, texts) -> str:
        return texts['probe_command'] % texts['ffprobe_path']

    def _get_convert_command(self, texts, SelectionCodecs, ffmpeg_path):

        _command_input = texts['convert_command'] % ffmpeg_path
        result = {}
        for enum in SelectionCodecs:
            result[enum.value] = ' '.join([_command_input, texts[enum.name], texts['output_command']])

        return result
        # MP3 OPTIONS -codec:a libmp3lame -q:a 1 -ar 44100 -ar 48000 -af "volume=10dB" -af "volume=1.5"

    def add_job(self, path: str, files: list) -> None:
        """
        Add files for converting
        :param path: Directory path
        :param files: File names
        """
        with self._convert_sem:
            self._jobs.append([path,
                               list(map(lambda file: [file, self._zero_time, self._zero_time], files))
                               ])
        for file in files:
            self.add_line([file, "0%", self._zero_time, self._zero_time])

    def _get_time_command(self, start, end):
        time = ''
        if start != self._zero_time or end != self._zero_time:
            time += '-ss %s' % start
            if end != self._zero_time:
                time += ' -to %s' % end
            time = '-sn %s ' % time
        return time

    def _convert_file(self, file_path, selection, start, end, command, i):
        # Receive new file extension based on strategy
        extension = self._extension[selection](file_path, i)
        output_file = self._get_output_file_path(extension, file_path)
        time = self._get_time_command(start, end)

        # If file already exists do nothing
        if exists(output_file):
            self.set_progress(i, "FILE ALREADY EXISTS")
        # Else convert
        elif extension:
            result = Popen(command.replace("input", file_path).replace("time", time).replace("output", output_file),
                           universal_newlines=True)
            info(result.communicate())
            self.set_progress(i, "100%")
            self.set_color_ok(i)

    def start_convert(self, selection):
        info(selection)

        # copy for thread safety
        with self._convert_sem:
            jobs = list(self._jobs)

        # Receive command based on strategy
        command = self._commands[selection]
        i = 0
        with Timer('CONVERT', log_function=info):
            with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
                for path, files in jobs:
                    convert_dir = join(path, self.convert_directory)
                    if not exists(convert_dir):
                        mkdir(convert_dir)
                    info("Convert: " + str(len(files)) + " files")

                    for file, start, end in files:
                        file_path = join(path, file)
                        executor.submit(self._convert_file, file_path, selection, start, end, command, i)

                        i += 1

    def reset(self):
        with self._convert_sem:
            self._jobs = []

    # +++ CONVERT STRATEGIES +++
    # TODO convert to temp path
    def _get_output_file_path(self, new_extension, file_path):
        file_path = list(split(file_path))
        file_name, _ = splitext(file_path[-1])
        file_path.pop(-1)
        file_path.append(file_name + '.' + new_extension)
        file_path.insert(-1, self.convert_directory)
        return join(*file_path)

    def _get_audio_codec(self, file_path: str) -> str:
        """
        Get codec via probe
        :param file_path: Input file location
        :return: Codec
        """
        command = self._input_command.replace("input", file_path)
        info("PROBING: " + command)
        audio_codec = getoutput(command)
        info("AUDIO CODEC: " + audio_codec)

        return audio_codec.strip()

    def _get_file_extension(self, file_path: str, i: int) -> (str, str):
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
            self.set_progress(i, "TYPE NOT FOUND")
            return ''

    def set_time(self, row, column, new_data):
        column -= 1
        if 0 < column < 3:
            with self._convert_sem:
                for i, (path, files) in enumerate(self._jobs):
                    if row < len(files):
                        self._jobs[i][1][row][column] = new_data
                        break
                    else:
                        row -= len(files)
            print(row, column, new_data)

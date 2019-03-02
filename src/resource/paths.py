# -*- coding: utf8 -*-
from logging import error
from utility.os_interface import get_absolute_path, exists
from src.resource.texts import SelectionCodecs

_ffmpeg_path = get_absolute_path('lib\\ffmpeg\\bin\\ffmpeg.exe')
if not exists(_ffmpeg_path):
    error('ffmpeg not found')

_ffprobe_path = get_absolute_path('lib\\ffmpeg\\bin\\ffprobe.exe')
if not exists(_ffprobe_path):
    error('ffprobe not found')

downloader_command = ['youtube-dl', '--no-check-certificate']  # , '-U'


_command_input = '"' + _ffmpeg_path + '" -i "input" -vn -sn -c:a '

commands = {SelectionCodecs.EXTRACT: _command_input + 'copy -map_metadata 0 -id3v2_version 3  "output"',
            SelectionCodecs.MP3: _command_input + 'libmp3lame -qscale:a 3 -map_metadata 0 -id3v2_version 3  "output"',
            SelectionCodecs.OPUS: _command_input + 'libopus -vbr on -b:a 128k -map_metadata 0 -id3v2_version 3  "output"'}
# MP3 OPTIONS -codec:a libmp3lame -q:a 1 -ar 44100 -ar 48000 -af "volume=10dB" -af "volume=1.5"

input_command = '"' + _ffprobe_path + '" -v error -select_streams ' \
                                     'a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 -i "input"'

file_path = 'D:/Downloads/Downloader/Neu mp4'
icon_path = './resources/icon.ico'

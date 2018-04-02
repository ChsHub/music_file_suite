# -*- coding: utf8 -*-
from logging import error
from utility.os_interface import get_absolute_path,exists


ffmpeg_path = get_absolute_path('lib\\ffmpeg\\bin\\ffmpeg.exe')
if not exists(ffmpeg_path):
    error('ffmpeg not found')

ffprobe_path = get_absolute_path('lib\\ffmpeg\\bin\\ffprobe.exe')
if not exists(ffprobe_path):
    error('ffprobe not found')

downloader_command = ['youtube-dl', '--no-check-certificate']  # , '-U'
path_to_download_dir = 'D:\\Downloads\\Downloader\\Neu mp4'

# TODO convert music to music
command_extract = ffmpeg_path+' -i "input" -vn -sn ' \
                  '-c:a copy -map_metadata 0 -id3v2_version 3  "output"'

command_best_mp3 = ffmpeg_path+' -i "input" -vn -sn ' \
                   '-c:a libmp3lame -qscale:a 3 -map_metadata 0 -id3v2_version 3  "output"'

command_best_opus = ffmpeg_path+' -i "input" -vn -sn ' \
                   '-c:a libopus -vbr on -b:a 128k -map_metadata 0 -id3v2_version 3  "output"'
# -codec:a libmp3lame -q:a 1 -ar 44100
# -ar 48000
# 48000
# -af "volume=10dB"
# -af "volume=1.5"

input_command = ffprobe_path+' -v error -select_streams ' \
                'a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 -i "input"'

file_path = 'D:/Downloads/Downloader/Neu mp4'

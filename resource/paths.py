# -*- coding: utf8 -*-

downloader_command = ['youtube-dl', '--no-check-certificate', '-U']
path_to_download_dir = 'D:\\Downloads\\Downloader\\Neu mp4'

converter_command = 'D:\\Making\\Python\\music_file_suite\\lib\\ffmpeg\\bin\\ffmpeg.exe -i "input" -vn -sn ' \
                    '-acodec copy -map_metadata 0 -id3v2_version 3  "output"'

converter_command_old = 'D:\\Making\\Python\\music_file_suite\\lib\\ffmpeg\\bin\\ffmpeg.exe -i "input" -vn -sn ' \
                    '-codec:a libmp3lame -q:a 1 -ar 44100 -map_metadata 0 -id3v2_version 3  "output.mp3"'
# -codec:a libmp3lame -q:a 1 -ar 44100
# 48000
# -af "volume=10dB"
# -af "volume=1.5"
input_command = 'D:\\Making\\Python\\music_file_suite\\lib\\ffmpeg\\bin\\ffprobe.exe -v error -select_streams ' \
                'a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 -i "input"'

file_path = 'D:/Downloads/Downloader/Neu mp4'

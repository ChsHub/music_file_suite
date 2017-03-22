# -*- coding: utf8 -*-

downloader_command = ['D:\\Making\\Python\\music_file_suite\\lib\\youtube-dl\\youtube-dl.exe', '--no-check-certificate', '-U']
path_to_download_dir = 'D:\\Downloads\\Downloader\\Neu mp4'

converter_command = 'D:\\Making\\Python\\music_file_suite\\lib\\ffmpeg\\bin\\ffmpeg.exe -i "input" -codec:a libmp3lame -q:a 0 -ar 44100 "output"'
# 48000
path_to_convert_dir = 'D:\\Downloads\\Downloader\\Neu mp3 need meta'

file_path = 'D:/Musik/New Alben/Bob Marley/Bob Marley & The Wailers/Legend'

# -*- coding: utf8 -*-
__author__ = 'christian'
import logging

import lib.utility.path_str as path_str
from lib.utility import os_interface as os_interface


class playlist_wpl:
    def __init__(self):
        return

    # filter src path
    def __get_new_track_path(self, old_track_path):
        old_track_path = old_track_path.split('"')[1].replace("D:\Musik", "").replace("..", "").replace('\\', "/")
        return "/home/christian/Musik" + old_track_path

    def get_files(self, path, playlist_name):

        if ".wpl" not in playlist_name[-4:]:
            logging.error("wrong playlist name", playlist_name)
            return None

        old_data = os_interface.read_file_data(path, playlist_name)
        if old_data is None:
            logging.error("empty playlist " + playlist_name)
            return None

        tracks_str = old_data.split("seq")
        tracks_str.pop()

        if (len(tracks_str) is 2):
            tracks = tracks_str[1].split("<media")
            del tracks[0]
            return map(path_str.get_file_name, map(self.__get_new_track_path, tracks))
        else:
            return None


class playlist_xspf:
    def __init__(self):
        return

    # climb hierarchy
    # add new tag to data
    def __step_up(self, new_data, tag, depth, backlog):
        depth += 1
        new_data += [depth * ' ' + '<' + tag + '>']
        backlog.append(tag)
        return depth

    # descend hierarchy
    # close xml tag
    def __step_down(self, new_data, depth, backlog):
        tag = backlog.pop()
        new_data += [depth * ' ' + '</' + tag + '>']
        return depth - 1

    # write data of one track
    def __write_track(self, new_data, track_path, depth, backlog):
        depth = self.__step_up(new_data, 'track', depth, backlog)
        depth = self.__step_up(new_data, 'location', depth, backlog)

        new_data += [(depth + 1) * ' ' + 'file://' + track_path]

        depth = self.__step_down(new_data, depth, backlog)
        depth = self.__step_down(new_data, depth, backlog)

    def generate_playlist(self, album_path, playlist_path, playlist_name, files):
        # initialize hierarchy
        depth = 0
        backlog = []

        # begin xml document
        new_data = ['<?xml version="1.0" encoding="UTF-8"?>']
        new_data += ['<playlist version="1" xmlns="http://xspf.org/ns/0/">']
        depth = self.__step_up(new_data, 'trackList', depth, backlog)

        # write xml data
        for file in files:
            self.__write_track(new_data, album_path + '/' + file, depth, backlog)

        # close xml document
        depth = self.__step_down(new_data, depth, backlog)
        new_data += ['</playlist>']

        data = "\n".join(new_data)

        os_interface.write_file_data(playlist_path, playlist_name, data)


class playlist_m3u:
    def __init__(self):
        return

    def generate_playlist(self, album_path, playlist_path, playlist_name, files, playlist_type):
        album_path = path_str.get_relative_path(playlist_path, album_path)
        files = [path_str.get_full_path(album_path, file) for file in files]
        data = "\n".join(files).replace("/", '\\')

        os_interface.write_file_data(playlist_path, playlist_name, data)


# GENERATE the playlist
def generate_playlist(album_path, playlist_path, playlist_name, files):
    playlist_type = playlist_name[-4:]
    if playlist_type in ".m3u" or playlist_type in ".pls":
        playlist_m3u().generate_playlist(album_path, playlist_path, playlist_name, files, playlist_type)
    elif playlist_type in ".xspf":
        playlist_xspf().generate_playlist(album_path, playlist_path, playlist_name, files)

# -*- coding: utf8 -*-

from logging import error

# TODO REMOVE UTILITY
from os.path import join

from utility.os_interface import write_file_data, read_file_data
from utility.path_str import get_relative_path


class playlist_wpl:
    def __init__(self):
        pass

    # filter src path
    def __get_new_track_path(self, old_track_path):
        old_track_path = old_track_path.split('"')[1].replace("D:\Musik", "").replace("..", "").replace('\\', "/")
        return "/home/christian/Musik" + old_track_path

    def get_files(self, path, playlist_name):

        if ".wpl" not in playlist_name[-4:]:
            error("wrong playlist name", playlist_name)
            return None

        old_data = read_file_data(path, playlist_name)
        if old_data is None:
            error("empty playlist " + playlist_name)
            return None

        tracks_str = old_data.split("seq")
        tracks_str.pop()

        if (len(tracks_str) is 2):
            tracks = tracks_str[1].split("<media")
            del tracks[0]
            return map(lambda name: name.split("\\")[-1].split("/")[-1], map(self.__get_new_track_path, tracks))
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

        write_file_data(playlist_path, playlist_name, data="\n".join(new_data))


def generate_playlist_m3u(album_path, playlist_path, playlist_name, files):
    album_path = get_relative_path(playlist_path, album_path)
    files = [join(album_path, file) for file in files]

    write_file_data(playlist_path, playlist_name, data="\n".join(files).replace("/", '\\'))


# GENERATE the playlist
def generate_playlist(album_path, playlist_path, playlist_name, files):
    if playlist_name.endswith('.m3u') or playlist_name.endswith('.pls'):
        generate_playlist_m3u(album_path, playlist_path, playlist_name, files)

    elif playlist_name.endswith('.xspf'):
        playlist_xspf().generate_playlist(album_path, playlist_path, playlist_name, files)

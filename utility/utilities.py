__author__ = 'Christian'
from os_interface import get_dir_list


def get_artist_and_album(album_path):

    temp = album_path.split("/")

    # split last element in list
    for x in temp.pop().split(" - "):
        temp.append(x)
    return (temp[-2], temp[-1])


def get_files(target_path, types):
    files = get_dir_list(target_path)
    files = filter(lambda x: x[-4:].lower() in types, files)

    return sorted(files)


def track_nr_int_to_str(nr):
    nr = str(nr)
    if len(nr) is 1:
        nr = "0" + nr
    return nr


def is_album_nr(x):
    return len(x) is 1 or len(x) is 2


# PLAYLIST
def get_playlist_name(artist, album):
    return artist + " - " + album + ".wpl"

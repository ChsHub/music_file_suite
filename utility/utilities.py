def get_artist_and_album(album_path):
    temp = album_path.split("/")

    # split last element in list
    for x in temp.pop().split(" - "):
        temp.append(x)
    return (temp[-2], temp[-1])


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

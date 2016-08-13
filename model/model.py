import lib.utility.utilities as utilities
import lib.utility.os_interface as os
from song import Song
import levenshtein
import playlists

class Model:
    _path_to_old_playlists = "D:\Musik\Wiedergabelisten win"
    _Controller = None
    _Songs = None

    def __init__(self, Controller):
        print("NEW MODEL")
        self._Controller = Controller

    def analyze_files(self, album_dir):
        # gather data from path
        files = utilities.get_mp3_files(album_dir)

        artist, album = utilities.get_artist_and_album(album_dir)
        # TODO: rename create_playlist_name
        playlist_name = utilities.get_playlist_name(artist, album)

        playlist_files = self.get_playlist_files(self._path_to_old_playlists, playlist_name)

        files = self.get_mp3_files_ordered(files, playlist_files)

        print("ANALYZE FILES")
        self._Songs = []
        for file, nr_in_playlist in files:
            self._Songs += [Song(file, album_dir, nr_in_playlist, artist, album)]


        print("RETURN GUI INSTRUCTION")
        self._Controller.update_view(self._Songs[-1].get_album_names())


    def change_files(self, is_album):

        for song in self._Songs:
            song.write_date(is_album)
        print("CHANGE FILES")
        print("RETURN FEEDBACK")

    def get_playlist_files(self, path_to_playlists, playlist_name):
        return playlists.playlist_wpl().get_files(path_to_playlists, playlist_name)


    # normal order if not possible
    def get_mp3_files_ordered(self, dir_files, playlist_files):
        if playlist_files is None:
            return [(dir_file, None) for dir_file in dir_files]

        i = 0
        result = []

        for play_file in playlist_files:

            i += 1
            if play_file in dir_files:
                result.append((play_file, i))
                dir_files.remove(play_file)
            else:
                play_file_short = play_file[:-4]
                for dir_file in dir_files:
                    if levenshtein.is_levenshtein_fit(play_file_short, dir_file[:-4]):
                        result.append((dir_file, i))
                        dir_files.remove(dir_file)
                        break

            if dir_files is None:
                return result

        # if more files in dir than in play list -> add them with track_num = None
        return result + [(dir_file, None) for dir_file in dir_files]
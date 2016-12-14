import lib.utility.utilities as utilities
import playlists


class Playlist:
    _path_to_old_playlists = "D:\Musik\Wiedergabelisten win"

    def __init__(self, files, album, artist):
        # TODO: rename create_playlist_name
        playlist_name = utilities.get_playlist_name(artist, album)
        playlist_files = self.get_playlist_files(self._path_to_old_playlists, playlist_name)

        files = self.get_mp3_files_ordered(files, playlist_files)

        raise NotImplementedError


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

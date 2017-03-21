import tag_interface as eyed3_interface
from meta_data import MetaData

class Tag_data:
    _audio_tag = None
    # meta data
    _album = None
    _album_artist = None
    _track_num = None
    _artist = None
    title = None

    def __init__(self, album_path, file_name):

        audio_tag = eyed3_interface.Tag(album_path, file_name)
        self._audio_tag = audio_tag

        album = audio_tag.get_album()
        if album:
            self._album = album

        album_artist = audio_tag.get_album_artist()
        if album_artist:
            self._album_artist = album_artist

        title = audio_tag.get_tag_title()
        if title:
            self.title = title

        track_num = audio_tag.get_tag_track_num()
        if track_num:
            self._track_num = track_num

        artist = audio_tag.get_artist()
        if artist:
            self._artist = artist

    def _set_new_tag(self, data):
        self._audio_tag.reset()
        self._audio_tag.set_tag_title(data[MetaData.Title])
        self._audio_tag.set_tag_artist(MetaData.Artist)
        self._audio_tag.set_tag_track_num(MetaData.TrackNum)
        self._audio_tag.set_tag_album_artist(MetaData.AlbumArtist)
        self._audio_tag.set_tag_album(MetaData.Album)

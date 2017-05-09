from meta_tags import MetaTags
from tag_interface import Tag
from logging import error, info


class Tag_data:
    # meta data
    _album = None
    _album_artist = None
    _track_num = None
    _artist = None
    title = None

    def __init__(self, album_path, file_name):

        self._audio_tag = Tag(album_path, file_name)

        album = self._audio_tag.get_album()
        if album:
            self._album = album

        album_artist = self._audio_tag.get_album_artist()
        if album_artist:
            self._album_artist = album_artist

        title = self._audio_tag.get_tag_title()
        if title:
            self.title = title

        track_num = self._audio_tag.get_tag_track_num()
        if track_num:
            self._track_num = track_num

        artist = self._audio_tag.get_artist()
        if artist:
            self._artist = artist

        info("READ: ", self._album, self._album_artist, self.title, self._track_num, self._artist)

    def _set_new_tag(self, data):

        if self._audio_tag and self._audio_tag.reset():
            self._audio_tag.set_tag_title(data[MetaTags.Title])
            self._audio_tag.set_tag_artist(data[MetaTags.Artist])
            self._audio_tag.set_tag_track_num(data[MetaTags.TrackNum])
            self._audio_tag.set_tag_album_artist(data[MetaTags.AlbumArtist])
            self._audio_tag.set_tag_album(data[MetaTags.Album])

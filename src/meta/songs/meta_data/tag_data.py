from src.meta.songs.meta_data.tag_interface import Tag
from src.meta.songs.meta_data.tag_interface_mp3 import TagMP3
from src.resource.meta_tags import MetaTags
from logging import error, info


class Tag_data:
    _audio_tag = None
    # meta data
    _album = ''
    _album_artist = ''
    _track_num = ''
    _artist = ''
    title = ''

    def __init__(self, album_path, file_name):

        if file_name.endswith(".mp3"):
            self._audio_tag = TagMP3(album_path, file_name)
        else:
            self._audio_tag = Tag(album_path, file_name)

        if not self._audio_tag:
            error("Couldn't retrieve audio tag")
            raise NotImplementedError

        if self._audio_tag._tag is None:
            error('Audio tag has no tag')

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

        info("READ: " + str(self._album) + " " + str(self._album_artist) + " "
             + str(self.title) + " " + str(self._track_num) + " " + str(self._artist))

    def set_new_tag(self, data):

        if self._audio_tag and self._audio_tag.reset():
            self._audio_tag.set_tag_title(data[MetaTags.Title])
            self._audio_tag.set_tag_artist(data[MetaTags.Artist])
            self._audio_tag.set_tag_track_num(data[MetaTags.TrackNum])
            self._audio_tag.set_tag_album_artist(data[MetaTags.AlbumArtist])
            self._audio_tag.set_tag_album(data[MetaTags.Album])
            self._audio_tag.save_tag()
            return True
        else:
            return False

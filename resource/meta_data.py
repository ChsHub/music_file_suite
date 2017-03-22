from enum import Enum


class MetaData(Enum):
    FileName = "File Name"
    Artist = "Artist"
    Title = "Title"
    TrackNum = "Track Nr."
    AlbumArtist = "Album Artist"
    Album = "Album"


class Types:
    MP3 = ".mp3"
    VIDEO = ".mp4,.webm,.flv"

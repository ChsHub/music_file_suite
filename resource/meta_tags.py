from enum import Enum


class MetaTags(Enum):
    FileName = "File Name"
    Artist = "Artist"
    Title = "Title"
    TrackNum = "Track Nr."
    AlbumArtist = "Album Artist"
    Album = "Album"


class FileTypes(Enum):
    MP3 = ".mp3"
    VIDEO = ".mp4,.webm,.flv"

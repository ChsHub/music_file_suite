from enum import Enum


class MetaTags(Enum):
    FileName = 'File Name'
    Artist = 'Artist'
    Title = 'Title'
    TrackNum = 'Track Nr.'
    AlbumArtist = 'Album Artist'
    Album = 'Album'


class SimpleTags(Enum):
    File = 'File'
    Progress = 'Progress'
    Start = 'Start'
    End = 'End'


class DownloadTags(Enum):
    File = 'File'
    Title = 'Title'
    Progress = 'Progress'
    Size = 'Size'


class FileTypes(Enum):
    MUSIC = '.ogg,.m4a,.mp3,.opus,.flac'
    VIDEO = '.mp4,.webm,.flv'

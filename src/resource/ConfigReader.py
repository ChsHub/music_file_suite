from configparser import ConfigParser
from os.path import abspath, exists


class ConfigReader(ConfigParser):
    def __init__(self):
        super().__init__()
        texts_path = 'resources/texts.cfg'

        if not exists(texts_path):
            self._write_default_settings(texts_path)

        self.read(abspath(texts_path))

    def _write_default_settings(self, texts_path: str) -> None:
        """
        Write default settings, if config file is missing
        """
        self['SelectionAlbum'] = {'DETECTED': 'as detected',
                                  'ALBUM': 'is Album',
                                  'RANDOM': 'is random'}
        self['SelectionMeta'] = {'NO_META': 'Ignore/overwrite meta data',
                                 'META': 'Use meta data'}
        self['SelectionCodecs'] = {'EXTRACT': 'Extract Audio only (Keep format)',
                                   'MP3': 'High quality mp3',
                                   'OPUS': 'Opus transparent'}

        self['Converter'] = {'convert_directory': 'CONVERTED',
                             'ffmpeg_path': 'lib\\ffmpeg\\bin\\ffmpeg.exe',
                             'convert_command': '"%%s" -i "input" -vn -sn -c:a ',
                             'EXTRACT': 'copy',
                             'MP3': 'libmp3lame -qscale:a 3',
                             'OPUS': 'libopus -vbr on -b:a 128k',
                             'output_command': '-map_metadata 0 -id3v2_version 3  "output"',
                             'ffprobe_path': 'lib\\ffmpeg\\bin\\ffprobe.exe',
                             'probe_command': '" -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 -i "input"'}

        self['Downloader'] = {'queue_path': './resources/youtube_links'}

        self['Window'] = {'SelectionTabs': ",".join(['Download', 'Convert', 'Meta', 'Config', 'About']),
                          'text_preview_change': 'Apply Change',
                          'text_preview_playlist': 'Create Playlist',
                          'text_download_input': 'Download YouTube',
                          'text_convert_input': 'Convert',
                          'text_start_convert': 'Start',
                          'text_codec_selection': 'Codec',
                          'text_file_input': 'Open File',
                          'text_view_title': 'Music Suite',
                          'text_set_download': 'Set Download Directory',
                          'text_open_file_title': 'Open Files',
                          'text_open_file': 'Music or Video',

                          'text_selection_meta': 'Previous Meta Data',
                          'text_selection_album': 'Is Album', }

        with open(texts_path, 'w') as configfile:
            self.write(configfile)

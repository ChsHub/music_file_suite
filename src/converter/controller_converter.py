from src.abstract.abstract_controller import AbstractController
from src.converter.abstract_converter import AbstractConverter
from src.converter.converter import Converter


class ControllerConverter(AbstractController, AbstractConverter):
    def __init__(self, view, config):
        AbstractController.__init__(self, view)
        self._converter = Converter(self, config['Converter'], config.SelectionCodecs, config.ffmpeg_path)
        AbstractConverter.__init__(self, self._converter)

    # Notify model

    def add_convert(self, path, files):
        if self._converter:
            self._submit(self._converter.add_job, path, files)

    def start_convert(self, selection):
        if self._converter:
            self._submit(self._converter.start_convert, selection)

    def reset_convert(self):
        if self._converter:
            self._submit(self._converter.reset)


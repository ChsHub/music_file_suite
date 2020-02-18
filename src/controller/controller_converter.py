from src.controller.generic_controller import GenericController
from src.model.apps.converter import Converter


class ControllerConverter(GenericController):
    def __init__(self, view, config):
        GenericController.__init__(self, view)
        self._converter = Converter(self, config['Converter'], config.SelectionCodecs, config.ffmpeg_path)

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


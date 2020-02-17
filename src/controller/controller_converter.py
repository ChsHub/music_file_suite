from src.controller.generic_controller import GenericController
from src.model.apps.converter import Converter


class ControllerConverter(GenericController):
    def __init__(self, view, config):
        GenericController.__init__(self)
        self._view = view
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

    # Notify view

    def set_convert_progress(self, id, percent):
        self._view.set_convert_progress(id, percent)

    def add_convert_line(self, line):
        self._view.add_convert_line(line)

    def update_meta_line(self, row, data):
        if self._view:
            self._view.update_preview_row(row, data)


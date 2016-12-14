from album import Album


class Model:
    _Controller = None

    _Album = None

    def __init__(self, Controller):
        self._Controller = Controller

    def analyze_files(self, album_dir):
        if self._Album:
            self._Album.set_inactive()
        self._Album = Album(album_dir, self.set_view)

    def set_data(self):
        self._Album.set_data()

    def set_view(self, data):
        self._Controller.set_view(data)

from album import Album

class Model:

    _Controller = None

    _Album = None

    def __init__(self, Controller):

        self._Controller = Controller

    def analyze_files(self, album_dir):

        self._Album = Album(album_dir)

    def set_data(self):
        self._Album.set_data()

    def get_data(self):
        return self._Album.get_data()





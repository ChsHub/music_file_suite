from album import Album

class Model:

    _Controller = None

    _Album = None

    def __init__(self, Controller):
        print("NEW MODEL")
        self._Controller = Controller

    def analyze_files(self, album_dir, is_album):

        self._Album = Album(album_dir)
        print("RETURN GUI INSTRUCTION")
        # TODO remove
        #self._Controller.update_view(self._Songs[-1].get_album_names())

    def set_data(self, is_album):
        self._Album.set_data(is_album)

    def get_data(self, is_album):
        return self._Album.get_data(is_album)





from cp_controller import Controller


class Main_Controller(Controller):
    def __init__(self):
        Controller.__init__(self, queue_size=100)

    def analyze_files(self, file_path):
        self.produce([self._Main_model.analyze_files, file_path])

    def set_data(self):
        if self._Main_model:
            return self._Main_model.set_data()

    def update_view(self, is_album):
        if self._Main_view:
            self.produce([self._Main_model.update_view, is_album])


    # called: Model -> Album -> Controller -> Window
    def set_view(self, data):
        if self._Main_view:
            self._Main_view.set_preview_data(data)

    def download(self, url):
        self.produce([self._Main_model.download_file, url])

    def convert_all(self, path):
        self.produce([self._Main_model.convert_file, path])

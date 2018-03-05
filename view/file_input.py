from wx import FileDialog, FD_OPEN, \
    FD_FILE_MUST_EXIST, FD_MULTIPLE, ID_CANCEL

from resource.meta_tags import FileTypes
from resource.texts import text_open_file_title, text_open_file
from view.standard_view.standard_input import StandardInput


class FileInput(StandardInput):

    def button_callback(self, event):
        file_types = FileTypes.VIDEO.value.replace(".", "*.").replace(",", ";")

        with FileDialog(self, text_open_file_title, "", "", wildcard=text_open_file +'('+ file_types+')|' + file_types,
                        style=FD_OPEN | FD_FILE_MUST_EXIST | FD_MULTIPLE) as dialog:
            if dialog.ShowModal() == ID_CANCEL:
                return  # the user changed their mind
            path = dialog.Directory
            files = dialog.Filenames

        self._callback(path=path, files=files)
        self._text_input.SetValue("")

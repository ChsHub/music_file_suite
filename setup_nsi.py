from utility.os_interface import read_file_data, write_file_data, depth_search_files
from utility.path_str import get_full_path

from src.resource.texts import text_view_title
from src.resource.paths import icon_path

script_name = "installer.nsi"
script = read_file_data("installer_template.nsi")

script = script.replace("App Name", text_view_title)
script = script.replace("logo.ico", icon_path)

files = depth_search_files(get_full_path('./dist', text_view_title), "")


write_file_data(".", script_name, script)

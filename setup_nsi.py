from os.path import join

from utility.os_interface import read_file_data, write_file_data, depth_search_files

from src.resource.ConfigReader import ConfigReader

icon_path = ConfigReader()['Window']['icon_path']
text_view_title = ConfigReader()['Window']['text_view_title']

script_name = "installer.nsi"
script = read_file_data("installer_template.nsi")

script = script.replace("App Name", text_view_title)
script = script.replace("logo.ico", icon_path)

files = depth_search_files(join('./dist', text_view_title), "")

write_file_data(".", script_name, script)

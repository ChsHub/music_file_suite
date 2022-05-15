from os import walk
from os.path import join
from pathlib import Path
from src.resource.ConfigReader import ConfigReader

icon_path = ConfigReader()['Window']['icon_path']
text_view_title = ConfigReader()['Window']['text_view_title']

script_name = "installer.nsi"
script = Path("installer_template.nsi").read_text('UTF-8')

script = script.replace("App Name", text_view_title)
script = script.replace("logo.ico", icon_path)

files = [file for root, _, files in walk(Path('./dist', text_view_title)) for file in files]

Path(script_name).write_text(script)

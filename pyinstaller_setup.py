# pyinstaller __main__.py --noconsole --onedir
# pyinstaller __main__.spec --noconsole
# EXE(
# Tree('.\\lib\\ffmpeg'),
# )
from subprocess import Popen
from utility.os_interface import delete_file

delete_file('build')
delete_file('dist')
process = Popen('pyinstaller __main__.spec')
# process = Popen('pyinstaller __main__.py --noconsole --onedir')

print(process.communicate(input="y"))
process = Popen('./dist/__main__/__main__.exe >log_files/execute.log')
print(process.communicate())

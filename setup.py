# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Tkinter. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# SimpleTkApp.py is a very simple type of Tkinter application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application
import os
import sys
from cx_Freeze import setup, Executable

build_exe_options = {"includes": ["tkinter"]}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
os.environ['TCL_LIBRARY'] = "C:\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python36-32\\tcl\\tk8.6"
executables = [Executable('main.py', base=base)]

setup(name='simple_Tkinter',
      version='0.1',
      description='Sample cx_Freeze Tkinter script',
      options={"build_exe": build_exe_options},
      install_requires=[],
      executables=executables)
# command:
# python setup.py bdist_msi

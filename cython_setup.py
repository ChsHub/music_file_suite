from distutils.core import setup
from Cython.Build import cythonize

setup(

  cythonize("model/songs/album.py"),
)
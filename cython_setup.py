from distutils.core import setup
from Cython.Build import cythonize
from utility.os_interface import depth_search_files, get_full_path, move_file, delete_file, make_directory

cython_path = "cython_src"
make_directory(cython_path)

for path, file in depth_search_files("src", ".py"):
    print(path, file)
    try:
        cythonize(get_full_path(path, file))
    except Exception as e:
        print(e)

    new_path = path.replace("src", cython_path)
    new_file = file.replace(".py", ".c")
    delete_file(new_path, new_file)
    move_file(old_path=path, new_path=new_path, file_name=new_file)

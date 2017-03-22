# -*- coding: utf8 -*-
# python3
from codecs import open
from logging import error, info
from os import rename, chdir, remove, getcwd, listdir, mkdir
from os.path import isdir, isfile, abspath, normpath
from re import escape, sub

import path_str


def make_directory(path):
    if not exists(path):
        mkdir(path)


def get_absolute_path(rel_path):
    return abspath(rel_path)


def delete_file(path, file_name):
    file_path = path_str.get_full_path(path, file_name)
    remove(file_path)


def change_dir(path):
    chdir(path)


def get_cwd():
    current_dir = getcwd()
    return path_str.get_clean_path(current_dir)

# from os import walk
# for x,z,y in walk("."):
#    print(x)
#    print(z)
#    print(y)
#    print()

# TODO use os.walk, os.path.join
def depth_search_paths(path, result):
    raise NotImplemented
    list = get_dir_list(path)
    i = 0
    if list is None:
        return result
    for dir in list:
        if '.' not in dir:
            i = i + 1
            result = depth_search_paths(path + "/" + dir, result)
    if i is 0:
        result.append(path)
    return result


def rename_files_replace(path, old, new, files):
    temp = []
    for x in files:
        a = x.replace(old, new)
        rename_file(path, x, a)
        temp.append(a)
    return temp


def get_dir_list(path):
    # try:
    if isdir(path):
        print(get_cwd())
        abs_path = get_absolute_path(path)
        print(abs_path)
        dir_list = listdir(abs_path)
        return sorted(dir_list)
    else:
        return []


def read_file_data(path, file_name):
    path = path_str.get_full_path(path, file_name)
    try:
        with open(path, 'r', 'utf-8') as f:
            data = f.read()
            f.close()
        return data

    except IOError as e:
        error("read_file_data " + path + " " + str(e))


def write_file_data(path, file_name, data, mode='w'):
    with open(path_str.get_full_path(path, file_name), mode, 'utf-8') as f:
        f.write(data)
        f.close()


def rename_file(path, old_file, new_file):
    path = path.replace("/", "\\")
    old_file_uni = old_file
    new_file_uni = new_file

    if new_file_uni == old_file_uni:
        return

    try:
        # TODO remove change dir
        change_dir(path)
        rename(old_file_uni, new_file_uni)
    except WindowsError as e:
        # TODO error on second rename
        error("set new file name", "old: " + old_file + " //  new: " + new_file)  # , e)


def replace_in_file_name(file_name, path, old, new=""):
    if old in file_name:
        new_name = file_name.replace(old, new)
        rename_file(path, file_name, new_name)
        return new_name
    else:
        return file_name


def save_input(path, file_name, var_name, var_data):
    data = read_file_data(path=path, file_name=file_name)
    try:
        my_regex = escape(var_name) + r".*[\n]"
        info("os_interface.save_input: " + path + " " + file_name)
        data = sub(my_regex, var_name + " = '" + var_data + "'\n", data)
        write_file_data(path=path,
                        file_name=file_name, data=data)
    except Exception as e:
        error(str(e))


def exists(path):
    return isfile(path) or isdir(path)


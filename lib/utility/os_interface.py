# -*- coding: utf8 -*-
# python3
__author__ = 'Christian'

import codecs
import logging
import os
import re
import path_str


def get_absolute_path(rel_path):
    # TODO fix ..
    return os.getcwd() + rel_path


def delete_file(path, file_name):
    file_path = path_str.get_full_path(path, file_name)
    os.remove(file_path)


def change_dir(path):
    os.chdir(path)


def get_cwd():
    current_dir = os.getcwd()
    return path_str.get_clean_path(current_dir)


def depth_search_paths(path, result):
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
    if os.path.isdir(path):
        dir_list = os.listdir(path)
        return dir_list
    else:
        return []
        # except WindowsError as e:
        #   log.logfile.handle_error("Windows Error", path, e)
        # return None


def read_file_data(path, file_name):
    path = path_str.get_full_path(path, file_name)
    try:
        with open(path, 'r') as f:
            data = f.read()
            f.close()
        return data

    except IOError as e:
        logging.error("read_file_data " + path + " " + str(e))


def write_file_data(path, file_name, data, mode='w'):
    change_dir(path)

    with codecs.open(file_name, mode, 'utf-8') as f:
        f.write(data)
        f.close()


def rename_file(path, old_file, new_file):
    path = path.replace("/", "\\")
    old_file_uni = old_file
    new_file_uni = new_file

    if new_file_uni == old_file_uni:
        return

    try:

        change_dir(path)
        os.rename(old_file_uni, new_file_uni)
    except WindowsError as e:
        # TODO error on second rename
        logging.error("set new file name", "old: " + old_file + " //  new: " + new_file)  # , e)


def replace_in_file(file, path, re, ne=""):
    if re in file:
        new_name = file.replace(re, ne)
        rename_file(path, file, new_name)
        return new_name
    else:
        return file


def save_input(path, file_name, var_name, var_data):
    data = read_file_data(path=path, file_name=file_name)
    try:
        my_regex = re.escape(var_name) + r".*[\n]"
        logging.info("os_interface.save_input: "+path+" "+file_name)
        data = re.sub(my_regex, var_name + " = '" + var_data + "'\n", data)
        write_file_data(path=path,
                file_name=file_name, data=data)
    except Exception as e:
        logging.error(str(e))

def exists(path):
    return os.path.isfile(path)

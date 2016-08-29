# -*- coding: utf8 -*-
__author__ = 'Christian'
import codecs
import logging
import os

import encoding
import path_str


def get_absolute_path(rel_path):
    # TODO fix ..
    return os.getcwd() + rel_path


def change_dir(path):
    os.chdir(encoding.f_decode(path))

def get_cwd():
    return path_str.get_clean_path(os.getcwd())

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
    dir_list = os.listdir(encoding.f_decode(path))
    return map(encoding.f_encode, dir_list)

    # except WindowsError as e:
    #   log.logfile.handle_error("Windows Error", path, e)
    # return None


def read_file_data(path, file_name):
    path = path_str.get_full_path(path, file_name)
    try:
        with codecs.open(encoding.f_decode(path), u'rb', u'UTF-8') as f:
            data = f.read()
            f.close()
        return encoding.f_encode(data)
        # return data

    except IOError as e:
        logging.error("read_file_data " + path + " " + str(e))


def write_file_data(path, file_name, data, mode=u'w'):
    change_dir(path)

    with open(encoding.f_decode(file_name), mode) as f:
        f.write(data)
        f.close()


def rename_file(path, old_file, new_file):
    path = path.replace("/", "\\")
    old_file_uni = encoding.f_decode(old_file)
    new_file_uni = encoding.f_decode(new_file)

    if new_file_uni in old_file_uni \
            and len(new_file_uni) is len(old_file_uni):
        return

    try:

        change_dir(path)
        os.rename(old_file_uni, new_file_uni)
    except WindowsError as e:
        logging.error("set new file name", "old: " + old_file + " //  new: " + new_file, e)


def replace_in_file(file, path, re, ne=""):
    if re in file:
        new_name = file.replace(re, ne)
        rename_file(path, file, new_name)
        return new_name
    else:
        return file

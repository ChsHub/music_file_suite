__author__ = 'Christian'
import encoding


# PATH FORMATTING

def get_clean_path(path):
    # TODO Remove second replace()
    return path.replace(u"\\", u"/").replace(u"//", u"/")


def get_full_path(path, file_name):

    return path + "/" + file_name


def get_relative_path(source, target):

    source = source.split("/")
    target = target.split("/")

    for x in range(len(source)):

        if not source[0] in target[0]:
            break
        else:
            src_token = source.pop(0)
            trg_token = target.pop(0)

    source = "./" + "/".join(['..' for x in source]) + "/"

    target = source + "/".join(target)

    return target


def change_file_name(file):
    rename_list = [("_", " "), ("(", " ("), ("Feat", "ft."), ("ft", "ft."), ("vs", "ft."), ("Vs.", "ft."), ("  ", " "),
                   ("..", "."), ("..", ".")]

    new_name = file
    for y in rename_list:
        new_name = new_name.replace(y[0], y[1])
    return new_name


def get_file_name(file_path):
    return file_path.split("\\")[-1].split("/")[-1]
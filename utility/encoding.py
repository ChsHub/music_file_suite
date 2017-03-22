# python3
# str in python3 is unicode


# input as byte str
def decode(input_byte, codec='UTF-8'):
    if type(input_byte) == str:
        raise TypeError
    if input_byte is not None:
        return input_byte.decode(codec).replace("&apos;", "\'")
    else:
        return None


# output unicode string
def encode(output_str, codec='UTF-8'):
    if type(output_str) != str:
        raise TypeError
    if output_str is not None:
        return output_str.encode(codec)
    else:
        return None


# python2
# (str in python2 is byte string)
# (unicode in python2 is unicode code points)
def f_decode(output_str):
    if type(output_str) != str:
        raise TypeError
    if output_str is not None:
        return output_str.decode('UTF-8')
    else:
        return None


def f_encode(input_uni):
    if type(input_uni) == str:
        raise TypeError
    if input_uni is not None:
        return input_uni.encode('UTF-8').replace("&apos;", "\'")
    else:
        return None

        # import sys
        # print(sys.getfilesystemencoding())

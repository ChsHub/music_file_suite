# python3
# str in python3 is unicode (python2 is byte string)
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

__author__ = 'Christian'
# python3

# str in python3 is unicode (python2 is byte string)
# input as byte str
def decode(input_byte):
    if input_byte is not None:
        return input_byte.decode('UTF-8').replace("&apos;", "\'")
    else:
        return None


# output unicode string
def encode(output_str):
    if output_str is not None:
        return output_str.encode('UTF-8')
    else:
        return None

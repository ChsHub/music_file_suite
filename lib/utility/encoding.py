__author__ = 'Christian'

def f_encode(input_uni):
    if input_uni is not None:
        return input_uni.encode('UTF-8').replace("&apos;", "\'")
    else:
        return None


def f_decode(output_str):
    if output_str is not None:
        return output_str.decode('UTF-8')
    else:
        return None

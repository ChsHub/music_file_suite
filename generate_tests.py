# python 3.6+

from os import walk
from os.path import join

from utility.os_interface import depth_search_files, get_cwd, is_file_type, make_directory
from re import findall

test_directory = 'generated_tests'
make_directory(test_directory)


def parse_file(path, file):
    re_classes = r'((?:\ {4}def.*:)|(?:class.*:))'  # classes and methods
    re_spaces = r'(\s{4})'

    with open(join(path, file), 'r') as f:
        lines = findall(re_classes, f.read())

    # add pass
    for i, line in enumerate(lines):
        if 'def' in line:
            intendations = len(findall(re_spaces, line)) + 1
            lines[i] += '\n' + '    ' * intendations + 'pass'

    generated_test = '\n'.join(lines)

    generated_test = 'from hypothesis import given, example' \
                     '\nfrom hypothesis.strategies import text' \
                     '\nfrom src.model.model import Model\n' \
                     'from tempfile import TemporaryDirectory\n' \
                     'from unittest import TestCase, main\n\n\n' + generated_test + \
                     "\n\nif __name__ == '__main__':\n    main()\n"

    new_file = join(get_cwd(), test_directory, 'test_' + file)
    with open(new_file, 'w') as generated:
        generated.write(generated_test)


path = join(get_cwd(), 'src')
for f_path, sub_dirs, files in walk(path):
    # exclude directories
    if not is_file_type(f_path, ['.git', 'docs', 'tests', 'build', 'documents', 'generate', test_directory]):
        for file_name in files:
            if is_file_type(file_name=file_name, types='.py'):
                parse_file(f_path, file_name)

# TODO generate tests

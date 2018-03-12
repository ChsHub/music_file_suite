#!/usr/bin/env python
import io
import re
from setuptools import setup, find_packages
import sys

with io.open('./__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name='music_suite',
    version=version,
    description='test',
    long_description=long_description,
    author='tsts',
    author_email='tst',
    license='Other',
    packages=find_packages(exclude=['docs', 'tests', 'build', 'documents', 'generate', 'generated_tests']),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Other',
    ],
    install_requires=["utility", "mutagen", "youtube-dl", "wxpython"],
    options={
        'app': {
            'formal_name': 'test',
            'bundle': 'tsts'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': [
                'toga-cocoa',
            ]
        },
        'linux': {
            'app_requires': [
                'toga-gtk',
            ]
        },
        'windows': {
            'app_requires': [
                'kivy'
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
                'toga-ios',
            ]
        },
        'android': {
            'app_requires': [
                'toga-android',
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
                'toga-django',
            ]
        },
    }
)

# >> Windows Power Shell
# Set-ExecutionPolicy UNRESTRICTED PROCESS

# python setup.py windows -s
# C:\\Python36-32\\python.exe setup.py windows -s
# C:\\Python35\\python.exe setup.py windows -s
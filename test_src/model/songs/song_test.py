import unittest

from hypothesis import given
from model.songs.song import Song

class TestSong(unittest.TestCase):

    def setUp(self):
        test_song = Song(None, None, None)


if __name__ == '__main__':
    unittest.main()
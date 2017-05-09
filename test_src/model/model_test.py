import unittest
from model import Model

class TestSong(unittest.TestCase):



    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_init__(self):
        #Model()
        pass

    def test_analyze_files(self):
        pass

    def test_set_data(self):
        pass

    def test_set_is_album(self):
        pass

    def test_set_is_meta(self):
        pass

    def test_download_file(self):
        pass

    def test_convert_file(self):
        pass


if __name__ == '__main__':
    unittest.main()

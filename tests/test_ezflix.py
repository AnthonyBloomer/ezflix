import unittest
import os
from random import randrange

from ezflix import Ezflix


class EzflixTests(unittest.TestCase):
    """
    This test class tests the Ezflix object.
    """

    def test_get_torrents(self):
        """
         This method tests the get_torrents function
         The test asserts the function returns a list that's > 0 and <= 20
        :return:
        """
        ezflix = Ezflix(query='Breaking Bad', limit=20)
        torrents = ezflix.get_torrents()
        self.assertTrue(0 <= len(torrents) <= 20)

    def test_get_magnet(self):
        """
        This method tests the get_magnet function.
        This test asserts the function returns a magnet link.
        :return:
        """
        ezflix = Ezflix(query='Breaking Bad', limit=20)
        torrents = ezflix.get_torrents()
        self.assertTrue(torrents > 0)
        self.assertTrue(ezflix.get_magnet(1) is not None)

    def test_get_subtitles(self):
        """
        This method tests the find_subtitles() function.
        This test asserts the function finds subtitles for the given search query.
        Since subliminal keeps a cache of subtitle files downloaded, this function takes a random result from the
        list and asserts we can find subtitles for that movie.
        :return:
        """
        ezflix = Ezflix(query='2017', media_type='movie', limit=20)
        torrents = ezflix.get_torrents()
        self.assertTrue(torrents > 0)
        random_index = randrange(0, len(torrents))
        first = torrents[random_index]['title']
        subtitles = ezflix.find_subtitles(first)
        self.assertIsNotNone(subtitles)
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        for f in file_list:
            if first in f:
                os.remove(f)

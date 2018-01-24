import unittest
import os
from ezflix import Ezflix


class EzflixTests(unittest.TestCase):
    def test_movie_get_torrents_by_quality(self):
        ezflix = Ezflix(query='Breaking Bad', limit=20, quality="720p")
        torrents = ezflix.get_torrents()
        for torrent in torrents:
            self.assertTrue("720" in torrent['title'])

        ezflix = Ezflix(query='Mad Max', media_type="movie", limit=20, quality="720p")
        torrents = ezflix.get_torrents()
        for torrent in torrents:
            self.assertTrue("720" in torrent['title'])

    def test_get_torrents(self):
        ezflix = Ezflix(query='Breaking Bad', limit=20)
        torrents = ezflix.get_torrents()
        self.assertTrue(0 <= len(torrents) <= 20)

    def test_get_magnet(self):
        ezflix = Ezflix(query='Breaking Bad', limit=20)
        torrents = ezflix.get_torrents()
        self.assertTrue(len(torrents) > 0)
        self.assertTrue(ezflix.get_magnet(1) is not None)

    def test_get_subtitles(self):
        ezflix = Ezflix(query='Mad Max', media_type='movie', limit=20)
        torrents = ezflix.get_torrents()
        self.assertTrue(len(torrents) > 0)
        movie_title = torrents[0]['title']
        subtitles = ezflix.find_subtitles(movie_title)
        self.assertIsNotNone(subtitles)
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        for f in file_list:
            if movie_title in f:
                os.remove(f)

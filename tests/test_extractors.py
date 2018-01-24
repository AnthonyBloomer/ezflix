import unittest
from ezflix.extractors import yts, eztv


class ExtractorTests(unittest.TestCase):

    def test_yts(self):
        torrents = yts(query_term='Goodfellas')
        self.assertTrue(len(torrents) > 0)
        self.assertTrue('Goodfellas' in torrents[0]['title'])

    def test_yts_limit(self):
        torrents = yts(query_term='Scarface', limit=1)
        self.assertTrue(len(torrents) == 1)

    def test_eztv(self):
        torrents = eztv(q='Breaking Bad', limit=20)
        self.assertTrue(len(torrents) > 0)
        self.assertTrue('Breaking Bad' in torrents[0]['title'])

    def test_eztv_limit(self):
        torrents = eztv(q='Breaking Bad', limit=1)
        self.assertTrue(len(torrents) == 1)

    def test_yts_quality(self):
        torrents = yts(query_term='Scarface', limit=1, quality='720p')
        self.assertTrue(len(torrents) > 0)
        first = torrents[0]
        self.assertTrue('720p' in first['title'])

    def test_eztv_quality(self):
        torrents = eztv(q='Breaking Bad', limit=20, quality='720p')
        self.assertTrue(len(torrents) > 0)
        self.assertTrue('Breaking Bad' in torrents[0]['title'])
        self.assertTrue('720p' in torrents[0]['title'])

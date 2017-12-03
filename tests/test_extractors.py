import unittest
from ezflix.extractors import yts, eztv


class ExtractorTests(unittest.TestCase):
    """
    This test class tests the extractors built into Ezflix.
    """

    def test_yts(self):
        """
        This method tests the yts function.
        The test asserts the function returns a list > 0 and the first result matches the search query.
        """
        torrents = yts(q='Goodfellas')
        self.assertTrue(len(torrents) > 0)
        self.assertTrue('Goodfellas' in torrents[0]['title'])

    def test_yts_limit(self):
        """
        This method tests the limiting in the yts function.
        The test asserts the function returns a list that is equal to the limit defined.
        """
        torrents = yts(q='Scarface', limit=1)
        self.assertTrue(len(torrents) == 2)

    def test_eztv(self):
        """
        This method tests the yts function.
        The test asserts the function returns a list > 0 and the first result matches the search query.
        """
        torrents = eztv(q='Breaking Bad', limit=20)
        self.assertTrue(len(torrents) > 0)
        self.assertTrue('Breaking Bad' in torrents[0]['title'])

    def test_eztv_limit(self):
        """
        This method tests the limiting in the eztv function.
        The test asserts the function returns a list that is equal to the limit defined.
        """
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

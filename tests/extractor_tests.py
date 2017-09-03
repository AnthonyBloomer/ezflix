import unittest
from ezflix.extractor import yts, eztv


class ExtractorTests(unittest.TestCase):
    def test_yts(self):
        """
        This method tests the yts function.
        The test asserts the function returns a list > 0 and the first result matches the search query.
        :return:
        """
        torrents = yts(q='Goodfellas')
        self.assertTrue(len(torrents) > 0)
        self.assertTrue('Goodfellas' in torrents[0]['title'])

    def test_eztv(self):
        """
        This method tests the yts function.
        The test asserts the function returns a list > 0 and the first result matches the search query.
        :return:
        """
        torrents = eztv(q='Breaking Bad', limit=20)
        self.assertTrue(len(torrents) > 0)
        self.assertTrue('Breaking Bad' in torrents[0]['title'])

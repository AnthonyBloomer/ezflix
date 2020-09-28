import unittest
import os
from ezflix import Ezflix
from ezflix.extractors import (
    eztv,
    yts,
    find_similar,
    search_tmdb_shows,
    get_external_id,
)


class ExtractorTest(unittest.TestCase):
    def test_yts(self):
        movie = yts("Scarface", debug=True)
        self.assertTrue(len(movie) > 0)
        similar = find_similar(movie[0]["id"])
        self.assertTrue(len(similar) > 0)

    def test_eztv(self):
        show = eztv("South Park", 1, debug=True)
        self.assertTrue(len(show) == 1)

    def test_eztv_by_quality(self):
        shows = eztv("South Park", 1, quality="720p", debug=True)
        for show in shows:
            self.assertIn("720", show["title"])

    def test_eztv_invalid_values(self):
        shows = eztv("poenloasd", 1, quality="720p", debug=True)
        self.assertIsNone(shows)

    def test_eztv_external_id(self):
        shows = search_tmdb_shows("Breaking Bad")
        self.assertIsNotNone(shows)
        self.assertIsNotNone(get_external_id(shows[0].id))


class EzflixTests(unittest.TestCase):
    def test_movie_get_torrents_by_quality(self):

        ezflix = Ezflix(
            query="Mad Max",
            media_type="movie",
            limit=20,
            quality="720p",
            debug=True,
            cli_mode=True,
        )
        torrents = ezflix.search()
        for torrent in torrents:
            self.assertIn("720", torrent["title"])

    def test_movie_get_similar(self):

        ezflix = Ezflix(
            query="Thin Red Line",
            media_type="movie",
            limit=20,
            quality="720p",
            debug=True,
            cli_mode=True,
        )
        torrents = ezflix.search()
        self.assertTrue(len(torrents) > 0)
        print(torrents)
        similar = ezflix.similar(1)
        self.assertTrue(len(similar) > 0)
        print(similar)

    def test_get_torrents(self):
        ezflix = Ezflix(
            query="Man in the high castle", limit=20, debug=True, quality="720p"
        )
        torrents = ezflix.search()
        self.assertTrue(0 <= len(torrents) <= 20)

    def test_get_magnet(self):
        ezflix = Ezflix(query="Man in the high castle", limit=20)
        torrents = ezflix.search()
        self.assertTrue(len(torrents) > 0)
        self.assertIsNotNone(ezflix.torrent_info(1))

    def test_get_subtitles(self):
        ezflix = Ezflix(query="Mad Max", media_type="movie", limit=20)
        torrents = ezflix.search()
        self.assertTrue(len(torrents) > 0)
        movie_title = torrents[0]["title"]
        print(movie_title)
        subtitles = ezflix.search_subtitles(movie_title)
        self.assertIsNotNone(subtitles)
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        for f in file_list:
            if movie_title in f:
                os.remove(f)

    def test_get_subtitles_invalid_title(self):
        ezflix = Ezflix(query="sklsos", media_type="movie", limit=20)
        subtitles = ezflix.search_subtitles("psl2232ssd2")
        self.assertIsNone(subtitles)

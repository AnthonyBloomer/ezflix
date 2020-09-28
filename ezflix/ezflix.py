from .extractors import eztv, yts, find_similar
import os
from halo import Halo


class Ezflix(object):
    def __init__(
        self,
        query,
        media_type="tv",
        limit=20,
        sort_by="seeds",
        sort_order="desc",
        quality=None,
        minimum_rating=None,
        language="en",
        page=1,
        debug=False,
        cli_mode=False,
    ):
        self._torrents = []
        self._query = query
        self._media_type = media_type
        self._limit = limit
        self._sort_by = sort_by
        self._sort_order = sort_order
        self._quality = quality
        self._minimum_rating = minimum_rating
        self._language = language
        self._page = page
        self._debug = debug
        self._cli_mode = cli_mode

    def torrent_info(self, val):
        if self._torrents is None or int(val) > len(self._torrents):
            return None
        for torrent in self._torrents:
            if torrent["id"] == int(val):
                return torrent
        return None

    def search_subtitles(self, media_title):
        os.system("subliminal download -l %s \"%s\"" % (self._language, media_title))
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        for f in file_list:
            if media_title in f:
                return f

        return None

    def similar(self, t_id):
        spinner = None
        if self._cli_mode:
            spinner = Halo(text="Searching...", spinner="dots")
            spinner.start()
        if self._media_type == "movie":
            torrent_info = self.torrent_info(t_id)
            if torrent_info is None:
                return
            self._torrents = find_similar(
                torrent_info["yts_id"], self._quality, self._limit
            )
        if self._cli_mode:
            spinner.stop()
        return self._torrents

    def search(self):
        spinner = None
        if self._cli_mode:
            spinner = Halo(text="Searching...", spinner="dots")
            spinner.start()
        if self._media_type == "tv":
            self._torrents = eztv(
                self._query.replace(" ", "-").lower(),
                page=self._page,
                limit=self._limit,
                quality=self._quality,
                debug=self._debug,
            )
        elif self._media_type == "movie":
            self._torrents = yts(
                q=self._query,
                limit=self._limit,
                sort_by=self._sort_by,
                sort_order=self._sort_order,
                quality=self._quality,
                minimum_rating=self._minimum_rating,
                page=self._page,
                debug=self._debug,
            )
        if self._cli_mode:
            spinner.stop()
        return self._torrents

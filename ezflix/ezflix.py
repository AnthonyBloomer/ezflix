from .extractors import eztv, yts
import os
from halo import Halo


class Ezflix(object):
    def __init__(self,
                 query,
                 media_type='tv',
                 limit=20,
                 sort_by='seeds',
                 sort_order='desc',
                 quality=None,
                 minimum_rating=None,
                 language='en'
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

    def get_magnet(self, val):
        for result in self._torrents:
            if result['id'] == int(val):
                return result
        return None

    def find_subtitles(self, title):
        os.system("subliminal download -l %s '%s'" % (self._language, title))
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        for f in file_list:
            if title in f:
                return f

        return None

    def get_torrents(self):
        spinner = Halo(text='Searching...', spinner='dots')
        spinner.start()
        if self._media_type == 'tv':
            self._torrents = eztv(self._query.replace(' ', '-').lower(), limit=self._limit, quality=self._quality)

        elif self._media_type == 'movie':
            self._torrents = yts(q=self._query,
                                 limit=self._limit,
                                 sort_by=self._sort_by,
                                 sort_order=self._sort_order,
                                 quality=self._quality,
                                 minimum_rating=self._minimum_rating
                                 )
        spinner.stop()
        spinner.clear()
        return self._torrents

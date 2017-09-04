from extractor import eztv, yts
import os


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
        self.torrents = []
        self.query = query
        self.media_type = media_type
        self.limit = limit
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.quality = quality
        self.minimum_rating = minimum_rating
        self.language = language

    def get_magnet(self, val):
        for result in self.torrents:
            if result['id'] == int(val):
                return result
        return None

    def find_subtitles(self, title):
        os.system("subliminal download -l %s '%s'" % (self.language, title))
        cur_dir = os.getcwd()
        file_list = os.listdir(cur_dir)
        for f in file_list:
            if title in f:
                return f
        return None

    def get_torrents(self):

        if self.media_type == 'tv':
            self.torrents = eztv(self.query.replace(' ', '-').lower(), limit=self.limit)

        elif self.media_type == 'movie':
            self.torrents = yts(q=self.query,
                                limit=self.limit,
                                sort_by=self.sort_by,
                                sort_order=self.sort_order,
                                quality=self.quality,
                                minimum_rating=self.minimum_rating
                                )

        return self.torrents

import argparse
from utils import cmd_exists, peerflix
import sys
import colorful
from extractor.yts import yts
from extractor.eztv import eztv

try:
    from urllib import quote_plus as quote_plus
except:
    from urllib import parse as quote_plus

supported_players = [
    'mpv',
    'vlc',
    'mplayer',
    'smplayer',
    'mpchc',
    'potplayer',
    'webplay',
    'omx'
]

sort_types = [
    'download_count',
    'like_count',
    'date_added',
    'seeds',
    'peers',
    'rating',
    'title',
    'year'
]

sort_orders = [
    'asc',
    'desc'
]

media_types = [
    'movie',
    'tv'
]

qualities = [
    '720p',
    '1080p',
    '3d'
]

p = argparse.ArgumentParser()

p.add_argument('media_type', help="The media type.", default='tv', nargs='?', choices=media_types)
p.add_argument('query', help="The search query.")
p.add_argument('--limit', help="The number of results to return.", default='20', nargs='?')
p.add_argument('--minimum_rating', help="Used to filter movie by a given minimum IMDb rating", nargs='?')
p.add_argument('--media_player', help="The media player.", default='mpv', nargs='?')
p.add_argument('--latest', help="Play the latest TV episode.", dest='latest', action='store_true')
p.add_argument('--subtitles', help="Load subtitles file.", dest='subtitles', action='store_true')
p.add_argument('--sort_by', help="Use this argument to sort the torrents.", default='seeds', nargs='?',
               choices=sort_types)
p.add_argument('--sort_order', help="Use this argument to set the sort order.", default='desc', nargs='?',
               choices=sort_orders)
p.add_argument('--quality', help="Use this argument to set the min quality.", default='720p', nargs='?',
               choices=qualities)

args = p.parse_args()

media_player = args.media_player

if not cmd_exists('peerflix'):
    sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')

if media_player not in supported_players:
    sys.exit('Media player not supported.')

if not cmd_exists('mpv') and media_player is 'mpv':
    media_player = 'vlc'

if not args.query:
    sys.exit(colorful.red("Search query not valid."))


class Ezflix(object):
    def __init__(self,
                 media_type,
                 search_query,
                 quality,
                 sort_by,
                 minimum_rating,
                 sort_order,
                 latest=False,
                 player='mpv',
                 limit=20,
                 subtitles=False):

        self.media_type = media_type
        self.search_query = search_query
        self.latest = latest
        self.player = player
        self.torrents = []
        self.limit = limit
        self.subtitles = subtitles
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.quality = quality
        self.minimum_rating = minimum_rating

    def get_magnet(self, val):
        for result in self.torrents:
            if result['id'] == int(val):
                return result
        return False

    def get_torrents(self):
        if self.media_type == 'tv':
            self.torrents = eztv(self.search_query.replace(' ', '-').lower(), limit=self.limit)

        elif self.media_type == 'movie':
            self.torrents = yts(q=quote_plus(self.search_query),
                                limit=self.limit,
                                sort_by=self.sort_by,
                                sort_order=self.sort_order,
                                quality=self.quality,
                                minimum_rating=self.minimum_rating
                                )

    def display(self):
        if self.torrents is None or not len(self.torrents) > 0:
            sys.exit(colorful.red('No results found.'))

        if self.latest:
            latest = self.torrents[0]
            print("Playing " + latest['title'])
            peerflix(latest['magnet'], self.player, self.media_type, self.subtitles)
            sys.exit()

        for result in self.torrents:
            print(colorful.bold('| ' + str(result['id'])) + ' | ' + result['title'])

    def select(self):
        print("Make selection: ")
        while True:
            read = raw_input()

            if read == 'quit':
                sys.exit()

            try:
                int_val = int(read)
            except:
                print(colorful.red('Invalid selection.'))
                continue

            magnet = self.get_magnet(int_val)

            if not magnet:
                print(colorful.red('Invalid selection.'))
                continue

            print("Playing " + magnet['title'])

            peerflix(magnet['magnet'], self.player, self.media_type, self.subtitles)


def main():
    ezflix = Ezflix(media_type=args.media_type,
                    search_query=args.query,
                    latest=args.latest,
                    player=media_player,
                    limit=int(args.limit),
                    subtitles=args.subtitles,
                    sort_by=args.sort_by,
                    sort_order=args.sort_order,
                    quality=args.quality,
                    minimum_rating=args.minimum_rating
                    )
    ezflix.get_torrents()
    ezflix.display()
    ezflix.select()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

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


class Ezflix:
    def __init__(self, media_type, search_query, latest=False, media_player='mpv', limit=20):
        self.media_type = media_type
        self.search_query = search_query
        self.latest = latest
        self.media_player = media_player
        self.torrents = []
        self.limit = limit

    def get_magnet(self, val):
        for result in self.torrents:
            if result['id'] == int(val):
                return result

    def get_torrents(self):
        if self.media_type == 'tv':
            self.torrents = eztv(self.search_query.replace(' ', '-').lower(), limit=self.limit)

        elif self.media_type == 'movie':
            self.torrents = yts(quote_plus(self.search_query), limit=self.limit)

    def display(self):
        if self.torrents is None or not len(self.torrents) > 0:
            sys.exit(colorful.red('No results found.'))

        if self.latest:
            latest = self.torrents[0]
            print("Playing " + latest['title'])
            peerflix(latest['magnet'], self.media_player, self.media_type)
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
                val = int(read)
            except ValueError:
                print(colorful.red('Expected int.'))
                continue

            magnet = self.get_magnet(val)
            print("Playing " + magnet['title'])
            peerflix(magnet['magnet'], self.media_player, self.media_type)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('media_type', help="The media type", default='tv', nargs='?', choices=['movie', 'tv', 'music'])
    p.add_argument('query', help="The search query.")
    p.add_argument('--limit', help="The number of results to return", default='20', nargs='?')
    p.add_argument('--media_player', help="The media player.", default='mpv', nargs='?')
    p.add_argument('--latest', help="Play the latest TV episode.", dest='latest', action='store_true')
    args = p.parse_args()
    media_player = args.media_player,

    if not cmd_exists('peerflix'):
        sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')

    if not cmd_exists('mpv') and args.media_player == 'mpv':
        print('MPV not found. Setting default player as vlc.')
        media_player = 'vlc'

    if len(args.query) == 0:
        sys.exit(colorful.red("Search query not valid."))

    ezflix = Ezflix(media_type=args.media_type,
                    search_query=args.query,
                    latest=args.latest,
                    media_player=media_player,
                    limit=int(args.limit))
    ezflix.get_torrents()
    ezflix.display()
    ezflix.select()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

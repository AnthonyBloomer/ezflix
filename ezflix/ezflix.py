import argparse
from utils import cmd_exists, peerflix
import sys
import colorful
from extractor.xtorrent import XTorrent
from extractor.yts import yts
from extractor.eztv import eztv

try:
    from urllib import quote_plus as quote_plus
except:
    from urllib import parse as quote_plus


class Ezflix:
    def __init__(self, media_type, search_query, latest=False):
        self.media_type = media_type
        self.search_query = search_query
        self.latest = latest
        self.need_magnet = False
        self.magnet = None

    def get_magnet(self, val, torrents):
        for result in torrents:
            if result['id'] == int(val):
                return result['magnet']

    def get_torrents(self):
        arr = []
        if self.media_type == 'tv':
            torrents = eztv(self.search_query.replace(' ', '-').lower())

            if torrents is None:
                xt = XTorrent(quote_plus(self.search_query), self.media_type)
                self.need_magnet = True
                return xt.get_torrents()

            return torrents

        elif self.media_type == 'movie':
            torrents = yts(quote_plus(self.search_query))

            if torrents is None:
                xt = XTorrent(quote_plus(self.search_query), self.media_type)
                self.need_magnet = True
                return xt.get_torrents()

            return torrents


        elif self.media_type == 'music':
            xt = XTorrent(quote_plus(self.search_query), self.media_type)
            self.need_magnet = True
            return xt.get_torrents()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('media_type', choices=['movie', 'tv', 'music'])
    p.add_argument('query')
    p.add_argument('latest', nargs='?', default='0')
    args = p.parse_args()
    media_player = 'mpv'

    if not cmd_exists('peerflix'):
        sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')
    if not cmd_exists('mpv'):
        print('MPV not found. Setting default player as vlc.')
        media_player = 'vlc'
    ezflix = Ezflix(args.media_type, args.query, args.latest)
    torrents = ezflix.get_torrents()
    for result in torrents:
        print(colorful.bold('| ' + str(result['id'])) + ' | ' + result['title'])

    while True:
        read = raw_input()

        if read == 'quit':
            sys.exit()

        try:
            val = int(read)
        except ValueError:
            print(colorful.red('Expected int.'))
            continue

        magnet = ezflix.get_magnet(val, torrents)
        peerflix(magnet, media_player, args.media_type)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

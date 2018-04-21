# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os
import sys

HERE = os.path.abspath(os.path.dirname(__file__))

version_ns = {}

with open(os.path.join(HERE, '__version__.py')) as f:
    exec (f.read(), {}, version_ns)


class Parser(object):
    def __init__(self):
        self._parser = ArgumentParser(prog='ezflix')
        self._supported_players = [
            'mpv',
            'vlc',
            'mplayer',
            'smplayer',
            'mpchc',
            'potplayer',
            'webplay',
            'omx',
            'airplay'
        ]

        self._sort_types = [
            'download_count',
            'like_count',
            'date_added',
            'seeds',
            'peers',
            'rating',
            'title',
            'year'
        ]

        self._sort_orders = [
            'asc',
            'desc'
        ]

        self._media_types = [
            'movie',
            'tv'
        ]

        self._qualities = [
            '720p',
            '1080p',
            '3d'
        ]
        self._add_arguments()

    def _add_arguments(self):
        self._parser.add_argument(
            'media_type',
            help="The media type.",
            default='tv',
            nargs='?',
            choices=self._media_types
        )

        self._parser.add_argument(
            'query',
            help="The search query."
        )

        self._parser.add_argument(
            '--limit',
            help="TThe limit of results per page that has been set",
            default='20',
            nargs='?'
        )

        self._parser.add_argument(
            '--minimum_rating',
            help="Used to filter movie by a given minimum IMDb rating",
            nargs='?'
        )

        self._parser.add_argument(
            '--media_player',
            help="The media player.",
            default='mpv',
            nargs='?',
            choices=self._supported_players
        )

        self._parser.add_argument(
            '--latest',
            help="Play the latest TV episode.",
            dest='latest',
            action='store_true'
        )

        self._parser.add_argument(
            '--subtitles',
            help="Load subtitles file.",
            dest='subtitles',
            action='store_true')

        self._parser.add_argument(
            '--sort_by',
            help="Sorts the results by choosen value",
            default='date_added',
            nargs='?',
            choices=self._sort_types
        )

        self._parser.add_argument(
            '--sort_order',
            help="Orders the results by either Ascending or Descending order",
            default='desc',
            nargs='?',
            choices=self._sort_orders
        )

        self._parser.add_argument(
            '--quality',
            help="Used to filter by a given quality.",
            nargs='?',
            choices=self._qualities
        )

        self._parser.add_argument(
            '--genre',
            help='Used to filter by a given genre (See http://www.imdb.com/genre/ for full list)'
        )

        self._parser.add_argument(
            '--remove',
            help='Remove files on exit.',
            default=True,
            dest='remove',
            action='store_true'
        )
        
        self._parser.add_argument(
            '--no_seeds',
            help='Include torrents that have no seeds',
            default=False,
            dest='no_seeds',
            action='store_true'
        )

        self._parser.add_argument(
            '--language',
            help='Language as IETF code. Set this argument to download subtitles in a given language.',
            default='en'
        )

        self._parser.add_argument(
            '-v',
            '--version',
            action='version',
            version="%(prog)s (" + version_ns['__version__'] + ")"
        )

    def error(self):
        print('''              
                ███████╗███████╗███████╗██╗     ██╗██╗  ██╗
                ██╔════╝╚══███╔╝██╔════╝██║     ██║╚██╗██╔╝
                █████╗    ███╔╝ █████╗  ██║     ██║ ╚███╔╝ 
                ██╔══╝   ███╔╝  ██╔══╝  ██║     ██║ ██╔██╗ 
                ███████╗███████╗██║     ███████╗██║██╔╝ ██╗
                ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝╚═╝  ╚═╝                                                                                        
        ''')
        print("Ezflix v" + version_ns['__version__'])
        self._parser.print_help()
        sys.exit(0)

    def parse(self):
        return self._parser.parse_args()

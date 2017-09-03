from utils import cmd_exists, peerflix
import sys
import colorful
from extractor.yts import yts
from extractor.eztv import eztv
from argument_parser import Parser
import os
import uuid

try:
    from urllib import quote_plus as quote_plus
except ImportError:
    from urllib import parse as quote_plus

parser = Parser()
args = parser.parse()

media_player = args.media_player

if not cmd_exists('peerflix'):
    sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')

if not cmd_exists('mpv') and args.media_player == 'mpv':
    media_player = 'vlc'

if not args.query:
    sys.exit(colorful.red("Search query not valid."))


def get_magnet(val, torrents):
    for result in torrents:
        if result['id'] == int(val):
            return result
    return


def get_torrents():
    torrents = []

    if args.media_type == 'tv':
        torrents = eztv(args.query.replace(' ', '-').lower(), limit=args.limit)

    elif args.media_type == 'movie':
        torrents = yts(q=quote_plus(args.query),
                       limit=args.limit,
                       sort_by=args.sort_by,
                       sort_order=args.sort_order,
                       quality=args.quality,
                       minimum_rating=args.minimum_rating
                       )

    return torrents


def display(torrents):
    if torrents is None or len(torrents) == 0:
        sys.exit(colorful.red('No results found.'))

    if args.latest:
        latest = torrents[0]
        print("Playing " + latest['title'])
        peerflix(latest['magnet'], media_player, args.media_type, args.subtitles, args.remove)
        sys.exit()

    for result in torrents:
        print(colorful.bold('| ' + str(result['id'])) + ' | ' + result['title'])


def select(torrents):
    print("Make selection: (Enter quit to close the program)")
    while True:
        read = raw_input()

        if read == 'quit':
            sys.exit()

        try:
            int_val = int(read)
        except ValueError:
            print(colorful.red('Invalid selection.'))
            continue

        magnet = get_magnet(int_val, torrents=torrents)

        if not magnet:
            print(colorful.red('Invalid selection.'))
            continue

        print("Playing " + magnet['title'])

        file_path = ''

        if args.subtitles:
            os.system("subliminal download -l en '%s'" % magnet['title'])
            cur_dir = os.getcwd()
            file_list = os.listdir(cur_dir)
            for f in file_list:
                if magnet['title'] in f:
                    file_path = f

        peerflix(magnet['magnet'], media_player, args.media_type, args.subtitles, args.remove, file_path)


def main():
    torrents = get_torrents()
    display(torrents)
    select(torrents)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

import argparse
import subprocess
import sys

from extractor.xtorrent import XTorrent
from extractor.yts import yts
from extractor.eztv import eztv

from color import Color


try:
    from urllib import quote_plus as quote_plus
except:
    from urllib import parse as quote_plus


def cmd_exists(cmd):
    return subprocess.call('type ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def peerflix(title, magnet_link, media_player, media_type):
    is_audio = '-a' if media_type == 'music' else ''
    print('Playing %s!' % title)
    subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" %s --%s' % (magnet_link, is_audio, media_player)])


if not cmd_exists('mpv'):
    print('MPV not found. Setting default player as vlc.')
    player = 'vlc'

if not cmd_exists('peerflix'):
    sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')


def search():
    print('Enter the search query: (media-type query)')
    input = raw_input()
    input = input.split()
    main(mt=input[0], q=' '.join(input[1:])) if len(input) > 0 else search()


def main(q=None, mt=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('media_type', choices=['movie', 'tv', 'music'])
    parser.add_argument('query')
    parser.add_argument('latest', nargs='?', default='0')
    args = parser.parse_args()
    query = args.query if q is None else q
    mt = args.media_type if mt is None else mt
    p = 'mpv'
    need_magnet = False
    found = False
    torrents = []
    xt = []

    if mt == 'tv':
        torrents = eztv(query.replace(' ', '-').lower())
        if not torrents:
            xt = XTorrent(quote_plus(query), mt)
            torrents = xt.get_torrents()
            need_magnet = True

    elif mt == 'movie':
        torrents = yts(quote_plus(query))

        if torrents is None:
            xt = XTorrent(quote_plus(query), mt)
            torrents = xt.get_torrents()
            need_magnet = True

    elif mt == 'music':
        xt = XTorrent(quote_plus(query), mt)
        torrents = xt.get_torrents()
        need_magnet = True

    if args.latest == 'latest':
        if torrents:
            if need_magnet:
                torrents = xt.get_magnet(1)
                if torrents:
                    peerflix(title=torrents[0], magnet_link=torrents[1], media_player=p, media_type=mt)
            else:
                latest = torrents[0]
                peerflix(title=latest['title'], magnet_link=latest['magnet'], media_player=p, media_type=mt)
        else:
            sys.exit('Latest not found.')
    else:
        if torrents:
            print('Select %s' % mt.title())
            for result in torrents:
                print ('%s| %s |%s %s%s%s' % (
                    Color.BOLD, result['id'], Color.ENDC, Color.OKBLUE, result['title'], Color.ENDC))
        else:
            sys.exit('%s%s%s' % (Color.FAIL, 'No results found.', Color.ENDC))

        while True:
            read = raw_input()

            if read == 'quit':
                sys.exit()
            elif read == 'search':
                search()

            try:
                val = int(read)
            except ValueError:
                print(Color.FAIL + 'Expected int.' + Color.ENDC)
                continue

            if torrents is not None:

                if need_magnet:
                    torrents = xt.get_magnet(val)
                    if torrents:
                        found = True
                        peerflix(torrents[0], torrents[1], p, mt)
                    else:
                        found = False

                else:
                    for result in torrents:
                        if result['id'] == int(read):
                            found = True
                            peerflix(result['title'], result['magnet'], p, mt)

            else:
                sys.exit(Color.FAIL + 'No results found.' + Color.ENDC)

            if not found:
                print(Color.FAIL + 'Invalid selection.' + Color.ENDC)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

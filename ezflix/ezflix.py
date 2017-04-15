import argparse
import subprocess
import sys
import colorful
from extractor.xtorrent import XTorrent
from extractor.yts import yts
from extractor.eztv import eztv

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


def parser():
    p = argparse.ArgumentParser()
    p.add_argument('media_type', choices=['movie', 'tv', 'music'])
    p.add_argument('query')
    p.add_argument('latest', nargs='?', default='0')
    return p.parse_args()


def search():
    print('Enter the search query: (media-type query)')
    query = raw_input()
    query = query.split()
    if len(query) >= 2:
        main(media_type=query[0], q=' '.join(query[1:]))
    else:
        search()


def main(q=None, media_type=None):
    args = parser()
    query = args.query if q is None else q
    media_type = args.media_type if media_type is None else media_type
    media_player = 'mpv'
    need_magnet = False
    found = False
    torrents = []
    xt = []

    if media_type == 'tv':
        torrents = eztv(query.replace(' ', '-').lower())
        if not torrents:
            xt = XTorrent(quote_plus(query), media_type)
            torrents = xt.get_torrents()
            need_magnet = True

    elif media_type == 'movie':
        torrents = yts(quote_plus(query))

        if torrents is None:
            xt = XTorrent(quote_plus(query), media_type)
            torrents = xt.get_torrents()
            need_magnet = True

    elif media_type == 'music':
        xt = XTorrent(quote_plus(query), media_type)
        torrents = xt.get_torrents()
        need_magnet = True

    if args.latest == 'latest':
        if not torrents:
            sys.exit(colorful.red('Latest not found.'))
        if need_magnet:
            torrents = xt.get_magnet(1)
            if torrents:
                peerflix(torrents[0], torrents[1], media_player, media_type)
            else:
                latest = torrents[0]
                peerflix(latest['title'], latest['magnet'], media_player, media_type)

    else:
        if not torrents:
            sys.exit(colorful.red('No results found.'))
        print('Select %s' % media_type.title())

        for result in torrents:
            print(colorful.bold('| ' + str(result['id'])) + ' | ' + result['title'])

        while True:
            read = raw_input()

            if read == 'quit':
                sys.exit()
            elif read == 'search':
                search()

            try:
                val = int(read)
            except ValueError:
                print(colorful.red('Expected int.'))
                continue

            if torrents is None:
                sys.exit(colorful.red('No results found.'))

            if need_magnet:
                torrents = xt.get_magnet(val)
                if torrents:
                    found = True
                    peerflix(torrents[0], torrents[1], media_player, media_type)
                else:
                    found = False

            else:
                for result in torrents:
                    if result['id'] == int(read):
                        found = True
                        peerflix(result['title'], result['magnet'], media_player, media_type)

            if not found:
                print(colorful.red('Invalid selection.'))


if __name__ == '__main__':
    try:
        if not cmd_exists('peerflix'):
            sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')
        if not cmd_exists('mpv'):
            print('MPV not found. Setting default player as vlc.')
            player = 'vlc'
        main()
    except KeyboardInterrupt:
        sys.exit()

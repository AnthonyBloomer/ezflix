import argparse
import sys
import subprocess
from color import Color
from yts import yts
from eztv import eztv
from xtorrent import XTorrent

try:
    from urllib import quote_plus as quote_plus
except:
    from urllib import parse as quote_plus


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def peerflix(title, magnet, player, media_type):
    is_audio = '-a' if media_type == 'music' else ''
    print('Playing %s!' % title)
    subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" %s --%s' % (magnet, is_audio, player)])


if not cmd_exists("mpv"):
    print('MPV not found. Setting default player as vlc.')
    player = 'vlc'

if not cmd_exists("peerflix"):
    sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')


def search():
    print("Enter the search query: (media-type query)")
    input = raw_input()
    input = input.split()
    main(media_type=input[0], q=" ".join(input[1:])) if len(input) > 0 else search()


def main(q=None, media_type=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('media_type', choices=["movie", "tv", "music"])
    parser.add_argument('query')
    parser.add_argument('latest', nargs='?', default='0')
    args = parser.parse_args()
    query = args.query if q is None else q
    media_type = args.media_type if media_type is None else media_type
    player = 'mpv'
    need_magnet = False
    found = False
    results = []
    xt = []

    if media_type == 'tv':
        results = eztv(query.replace(' ', '-').lower())
        if not results:
            xt = XTorrent(quote_plus(query), media_type)
            results = xt.get_torrents()
            need_magnet = True

    elif media_type == 'movie':
        results = yts(quote_plus(query))

        if results is None:
            xt = XTorrent(quote_plus(query), media_type)
            results = xt.get_torrents()
            need_magnet = True

    elif media_type == 'music':
        xt = XTorrent(quote_plus(query), media_type)
        results = xt.get_torrents()
        need_magnet = True

    if args.latest == "latest":
        if results:
            if need_magnet:
                results = xt.get_magnet(1)
                if results:
                    peerflix(results[0], results[1], player, media_type)
            else:

                latest = results[0]
                peerflix(latest['title'], latest['magnet'], player, media_type)
        else:

            sys.exit('Latest not found.')
    else:

        if results:
            print('Select %s' % media_type.title())
            for result in results:
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

            if results is not None:

                if need_magnet:
                    results = xt.get_magnet(val)
                    if results:
                        found = True
                        peerflix(results[0], results[1], player, media_type)
                    else:
                        found = False

                else:
                    for result in results:
                        if result['id'] == int(read):
                            found = True
                            peerflix(result['title'], result['magnet'], player, media_type)

            else:
                sys.exit(Color.FAIL + 'No results found.' + Color.ENDC)

            if not found:
                print(Color.FAIL + 'Invalid selection.' + Color.ENDC)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

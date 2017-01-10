import argparse
import sys
import subprocess

try:
    from urllib import quote_plus
except:
    from urllib import parse

from sources.eztv import eztv
from sources.xtorrent import xtorrent
from sources.yts import yts

parser = argparse.ArgumentParser()
parser.add_argument('media_type', nargs='?', choices=["movie", "tv", "music"], default='tv')
parser.add_argument('query')
parser.add_argument('latest', nargs='?', default='0')
args = parser.parse_args()


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def peerflix(title, magnet, player, mt):
    is_audio = '-a' if mt == 'music' else ''
    print('Playing %s!' % title)
    subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" %s --%s' % (magnet, is_audio, player)])


def main(q=None, mt=None):
    query = args.query if q is None else q
    mt = args.media_type if mt is None else mt
    player = 'mpv'

    if not cmd_exists("mpv"):
        print 'MPV not found. Defaulting to vlc.'
        player = 'vlc'

    if not cmd_exists("peerflix"):
        sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')

    results = []

    if mt == 'tv':
        results = eztv(query.replace(' ', '-').lower())

    elif mt == 'movie':
        try:
            results = yts(quote_plus(query))
        except:
            results = yts(parse.quote_plus(query))

        if results is None:
            try:
                results = xtorrent(quote_plus(query), mt)
            except:
                results = xtorrent(parse.quote_plus(query), mt)

    elif mt == 'music':
        try:
            results = xtorrent(quote_plus(query), mt)
        except:
            results = xtorrent(parse.quote_plus(query), mt)

    if args.latest == "latest":
        latest = results[0]
        peerflix(latest['title'], latest['magnet'], player, mt)

    else:
        if results:
            print('Select %s' % mt.title())
            for result in results:
                print ('%s| %s |%s %s%s%s' % (
                    Color.BOLD, result['id'], Color.ENDC, Color.OKBLUE, result['title'], Color.ENDC))
        else:
            sys.exit('%s%s%s' % (Color.FAIL, 'No results found.', Color.ENDC))

        while True:
            read = raw_input()

            if read == 'quit':
                sys.exit()
            if read == 'search':
                print("Enter the search query: (media-type query)")
                search = raw_input()
                search = search.split()
                main(mt=search[0], q=" ".join(search[1:]))

            try:
                val = int(read)
            except ValueError:
                print(Color.FAIL + 'Expected int.' + Color.ENDC)
                continue

            found = False

            if results is not None:
                for result in results:
                    if result['id'] == int(read):
                        found = True
                        peerflix(result['title'], result['magnet'], player, mt)

            else:
                sys.exit(Color.FAIL + 'No results found.' + Color.ENDC)

            if not found:
                print(Color.FAIL + 'Invalid selection.' + Color.ENDC)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

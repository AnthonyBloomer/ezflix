import sys
import argparse
import subprocess
from extractor.eztv import eztv
from extractor.xtorrent import xtorrent
from extractor.yts import yts

try:
    from urllib import quote_plus
except:
    from urllib import parse

parser = argparse.ArgumentParser()
parser.add_argument('media_type', choices=["movie", "tv", "music"])
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


def peerflix(title, magnet, player, media_type):
    is_audio = '-a' if media_type == 'music' else ''
    print('Playing %s!' % title)
    subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" %s --%s' % (magnet, is_audio, player)])


def search():
    print("Enter the search query: (media-type query)")
    input = raw_input()
    input = input.split()
    if len(input) > 0:
        main(media_type=input[0], q=" ".join(input[1:]))
    else:
        search()


def main(q=None, media_type=None):
    query = args.query if q is None else q
    media_type = args.media_type if media_type is None else media_type
    player = 'mpv'

    if not cmd_exists("mpv"):
        print('MPV not found. Setting default player as vlc.')
        player = 'vlc'

    if not cmd_exists("peerflix"):
        sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')

    results = []

    if media_type == 'tv':
        results = eztv(query.replace(' ', '-').lower())
        if not results:
            try:
                results = xtorrent(quote_plus(query), media_type)
            except:
                results = xtorrent(parse.quote_plus(query), media_type)

    elif media_type == 'movie':

        try:
            results = yts(quote_plus(query))
        except:
            results = yts(parse.quote_plus(query))

        if results is None:
            try:
                results = xtorrent(quote_plus(query), media_type)
            except:
                results = xtorrent(parse.quote_plus(query), media_type)

    elif media_type == 'music':
        try:
            results = xtorrent(quote_plus(query), media_type)
        except:
            results = xtorrent(parse.quote_plus(query), media_type)

    if args.latest == "latest":
        if results:
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
            if read == 'search':
                search()
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

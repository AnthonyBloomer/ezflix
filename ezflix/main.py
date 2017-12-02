from .utils import cmd_exists, peerflix
import sys
import colorful
from .argument_parser import Parser
from .ezflix import Ezflix
from prettytable import PrettyTable
from builtins import input

parser = Parser()
args = parser.parse()

media_player = args.media_player

if not cmd_exists('peerflix'):
    sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')

if not cmd_exists('mpv') and args.media_player == 'mpv':
    media_player = 'vlc'

if not args.query:
    sys.exit(colorful.red("Search query not valid."))


def main():
    ezflix = Ezflix(query=args.query,
                    media_type=args.media_type,
                    limit=args.limit,
                    sort_by=args.sort_by,
                    sort_order=args.sort_order,
                    quality=args.quality,
                    minimum_rating=args.minimum_rating,
                    language=args.language
                    )

    torrents = ezflix.get_torrents()
    if torrents is None or len(torrents) == 0:
        sys.exit(colorful.red('No results found.'))
    if args.latest:
        latest = torrents[0]
        file_path = ''
        if args.subtitles:
            file_path = ezflix.find_subtitles(latest['title'])
        print("Playing " + latest['title'])
        peerflix(latest['magnet'], media_player, args.media_type, args.subtitles, args.remove, file_path)
        sys.exit()
    row = PrettyTable()
    row.field_names = ["Id", "Torrent"]
    row.align = 'l'
    for result in torrents:
        row.add_row([result['id'], result['title']])
    print(row)
    print(colorful.bold("Make selection: (Enter quit to close the program)"))
    while True:
        read = input()
        if read == 'quit':
            sys.exit()
        try:
            int_val = int(read)
        except (ValueError, TypeError) as error:
            print(colorful.red('Invalid selection.'))
            continue
        magnet = ezflix.get_magnet(int_val)
        if not magnet:
            print(colorful.red('Invalid selection.'))
            continue
        print("Playing " + magnet['title'])
        file_path = ''
        if args.subtitles:
            file_path = ezflix.find_subtitles(magnet['title'])
        peerflix(magnet['magnet'], media_player, args.media_type, args.subtitles, args.remove, file_path)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

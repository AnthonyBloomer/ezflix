from .utils import cmd_exists, peerflix
import sys
import colorful
from .argument_parser import Parser
from .ezflix import Ezflix
from prettytable import PrettyTable
from builtins import input
import logging
import time

logging.basicConfig()
logger = logging.getLogger(__file__)

if sys.version_info < (2, 7):
    logger.error('You need Python 2.7 or later\n')
    sys.exit(1)

parser = Parser()

if len(sys.argv) == 1:
    parser.error()
    sys.exit(0)

args = parser.parse()

media_player = args.media_player

if not cmd_exists('peerflix'):
    sys.exit('This program requires Peerflix. https://github.com/mafintosh/peerflix')

if not cmd_exists('mpv') and args.media_player == 'mpv':
    logger.warning("In ezflix, the default player is mpv. It will fallback to vlc if mpv isn't found. "
                   "You can use the media_player argument to set your media player.")
    media_player = 'vlc'

if not (args.query and args.query.strip()):
    sys.exit(colorful.red("Search query not valid."))


def search(page=1, term=None):
    global ezflix
    ezflix = Ezflix(query=args.query if term is None else term,
                    media_type=args.media_type,
                    limit=int(args.limit),
                    sort_by=args.sort_by,
                    sort_order=args.sort_order,
                    quality=args.quality,
                    minimum_rating=args.minimum_rating,
                    language=args.language,
                    page=page
                    )
    torrents = ezflix.get_torrents()
    if torrents is None or len(torrents) == 0:
        sys.exit(colorful.red('No results found.'))
    if args.latest:
        latest = torrents[0]
        file_path = ezflix.find_subtitles(latest['title']) if args.subtitles else None
        print("Playing " + latest['title'])
        time.sleep(2.5)
        peerflix(latest['magnet'], media_player, args.media_type, args.subtitles, args.remove, file_path)
        sys.exit()
    row = PrettyTable()
    row.field_names = ["Id", "Torrent", "Seeds", "Peers", "Released"]
    row.align = 'l'
    t = 0
    for result in torrents:
        if not (result['seeds'] == 0 or result['seeds'] is None) or args.no_seeds is True:
            row.add_row([result['id'], result['title'], result['seeds'], result['peers'], result['release_date']])
            t += 1
    if t > 0 or args.no_seeds:
        print(row) 
    else: 
        print(colorful.red("No results found."))
        sys.exit(0)


def main():
    page = 1
    search(page)
    print(colorful.bold("Make selection (Select the ID of the media you want to stream):"))
    print("Enter 'quit' to close the program.")
    print("Enter 'next' to see the next page of movies.")
    print("Enter 'prev' to see the previous page of movies.")
    print("Enter 'search' to refine your search.")
    while True:
        read = input()
        if read == 'quit':
            sys.exit()
        elif read == 'search':
            refined_query = input("Enter search query: ")
            search(page=1, term=refined_query)
            continue
        elif read == 'next':
            page += 1
            search(page)
            continue
        elif read == 'prev':
            if page > 1:
                page -= 1
                search(page)
            continue
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
        file_path = ezflix.find_subtitles(magnet['title']) if args.subtitles else None
        peerflix(magnet['magnet'], media_player, args.media_type, args.subtitles, args.remove, file_path)
        sys.exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)

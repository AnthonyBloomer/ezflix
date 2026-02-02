from prompt_toolkit.styles import Style

from .utils import cmd_exists, peerflix
import sys
import colorful
from .argument_parser import EzflixParser
from .ezflix import Ezflix
from prettytable import PrettyTable
from prompt_toolkit import PromptSession
import time
import subprocess
from prompt_toolkit.completion import WordCompleter


if sys.version_info < (2, 7):
    sys.exit("You need Python 2.7 or later\n")

parser = EzflixParser()

if len(sys.argv) == 1:
    parser.error()
    sys.exit(0)

args = parser.parse()

media_player = args.media_player
debug = args.debug

if not cmd_exists("peerflix"):
    sys.exit("This program requires Peerflix. https://github.com/mafintosh/peerflix")

if not cmd_exists("mpv") and args.media_player == "mpv":
    print(
        colorful.bold(
            "In ezflix, the default player is mpv. It will fallback to vlc if mpv isn't found. "
            "You can use the media_player argument to set your media player."
        )
    )
    media_player = "vlc"
if not cmd_exists(media_player):
    print(
        colorful.bold(
            f"not suported command {media_player} choosing default for peerflix(web player)"
        )
    )
    media_player ="w"
if not (args.query and args.query.strip()):
    sys.exit(colorful.red("Search query not valid."))


def main():
    style = Style.from_dict(
        {
            "completion-menu.completion": "bg:#008888 #ffffff",
            "completion-menu.completion.current": "bg:#00aaaa #000000",
            "scrollbar.background": "bg:#88aaaa",
            "scrollbar.button": "bg:#222222",
        }
    )
    completer = WordCompleter(
        ["next", "prev", "search", "info", "similar", "trailer", "imdb", "quit"]
    )
    session = PromptSession(completer=completer, style=style)
    p = 1
    res = search(p)
    if not res:
        sys.exit(0)
    if not args.no_menu:
        display_menu()
    while True:

        try:
            i = session.prompt("> ", completer=completer)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        if i == "quit":
            sys.exit()
        elif i == "search":
            refined_query = input("Enter search query: ")
            search(page=1, term=refined_query)

            continue
        elif i == "next":
            p += 1
            search(p)
            continue
        elif i == "prev":
            if p > 1:
                p -= 1
                search(p)
            continue
        elif "info" in i:
            media_info(i)
            continue
        elif "similar" in i:
            similar(i)
            continue
        elif "trailer" in i:
            play_trailer(i)
            continue
        elif "imdb" in i:
            open_imdb_page(i)
            continue
        if not str.isdigit(i):
            print(colorful.red("Invalid selection."))
            continue
        magnet = ezflix.torrent_info(int(i))
        if not magnet:
            print(colorful.red("Invalid selection."))
            continue
        print("Playing " + magnet["title"])
        file_path = ezflix.search_subtitles(magnet["title"]) if args.subtitles else None
        peerflix(magnet["link"], media_player, args.subtitles, args.remove, file_path)
        sys.exit()


def display_menu():
    pt = PrettyTable()
    pt.field_names = [
        "Help Menu : Pass --no-menu if you don't want to display this menu on program startup."
    ]
    pt.align = "l"
    pt.add_row(["Enter the ID of the media you want to stream."])
    pt.add_row(["Enter 'next' to see the next page of movies."])
    pt.add_row(["Enter 'prev' to see the previous page of movies."])
    pt.add_row(["Enter 'search' to refine your search."])
    pt.add_row(
        ["Enter 'info' and the id of the torrent to get the movie/tv show overview."]
    )
    pt.add_row(["Enter 'trailer' and the id of the torrent to play the movie trailer."])
    pt.add_row(["Enter 'similar' and the id of the torrent to find similar movies."])
    pt.add_row(
        ["Enter 'imdb' and the id of the torrent to open the imdb media webpage."]
    )
    pt.add_row(["Enter 'quit' to close the program."])
    print(pt)


def display_table(torrents):
    pt = PrettyTable()
    pt.field_names = ["Id", "Torrent", "Seeds", "Peers", "Released", "Rating", "Genre"]
    pt.align = "l"
    t = 0
    for result in torrents:
        if (
            not (result["seeds"] == 0 or result["seeds"] is None)
            or args.no_seeds is True
        ):
            pt.add_row(
                [
                    result["id"],
                    result["title"],
                    result["seeds"],
                    result["peers"],
                    result["release_date"],
                    result["rating"],
                    result["genre"],
                ]
            )
            t += 1
    if t > 0 or args.no_seeds:
        print(pt)
    else:
        print(colorful.red("No results found."))
        sys.exit(0)


def search(page=1, term=None):
    global ezflix
    ezflix = Ezflix(
        query=args.query if term is None else term,
        media_type=args.media_type,
        limit=int(args.limit),
        sort_by=args.sort_by,
        sort_order=args.sort_order,
        quality=args.quality,
        minimum_rating=args.minimum_rating,
        language=args.language,
        page=page,
        debug=debug,
        cli_mode=True,
    )
    torrents = ezflix.search()
    if torrents is None or len(torrents) == 0:
        print(colorful.red("No results found."))
        return False
    if args.latest:
        latest = torrents[0]
        file_path = ezflix.search_subtitles(latest["title"]) if args.subtitles else None
        print("Playing " + latest["title"])
        time.sleep(2.5)
        peerflix(latest["link"], media_player, args.subtitles, args.remove, file_path)
        sys.exit()
    display_table(torrents)
    return True


def media_info(user_input):
    sp = user_input.split()
    if not len(sp) > 1 or not str.isdigit(sp[1]):
        print(
            colorful.red(
                "Incorrect usage. Enter 'info' and the id of the torrent to get the movie/tv show overview."
            )
        )
        return
    torrent_info = ezflix.torrent_info(sp[1])
    if torrent_info is None:
        print(colorful.red("Invalid selection."))
        return
    print(torrent_info["overview"])


def similar(user_input):
    if args.media_type == "tv":
        print(colorful.red("Currently, movie torrents are only supported."))
        return
    sp = user_input.split()
    if not len(sp) > 1 or not str.isdigit(sp[1]):
        print(
            colorful.red(
                "Incorrect usage. Enter 'similar' and the id of the torrent to find similar movies."
            )
        )
        return
    torrents = ezflix.similar(sp[1])
    display_table(torrents)


def play_trailer(user_input):
    if args.media_type == "tv":
        print(colorful.red("Currently, movie torrents are only supported."))
        return
    sp = user_input.split()
    if not len(sp) > 1 or not str.isdigit(sp[1]):
        print(
            colorful.red(
                "Incorrect usage. Enter 'trailer' and the id of the torrent to play the movie trailer."
            )
        )
        return
    torrent_info = ezflix.torrent_info(sp[1])
    if torrent_info is None:
        print(colorful.red("Invalid selection."))
        return
    trailer = torrent_info["trailer"]
    if not trailer:
        print(colorful.red("No trailer found."))
        return
    geometry = "50%"
    subprocess.Popen(
        [
            "/bin/bash",
            "-c",
            "%s https://www.youtube.com/watch?v=%s --geometry=%s"
            % (media_player, trailer, geometry),
        ]
    )


def open_imdb_page(user_input):
    sp = user_input.split()
    if not len(sp) > 1 or not str.isdigit(sp[1]):
        print(
            colorful.red(
                "Incorrect usage. Enter 'imdb' and the id of the torrent to open the imdb page for the movie."
            )
        )
        return
    torrent_info = ezflix.torrent_info(sp[1])
    if torrent_info is None:
        print(colorful.red("Invalid selection."))
        return
    imdb = torrent_info["imdb"]
    if not imdb:
        print(colorful.red("No imdb found."))
        return
    subprocess.Popen(["/bin/bash", "-c", "open https://www.imdb.com/title/%s/" % imdb])


if __name__ == "__main__":
    main()

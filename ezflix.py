import subprocess
import argparse
from bs4 import BeautifulSoup
import requests
import sys
from urllib import quote_plus

parser = argparse.ArgumentParser()
parser.add_argument('media_type', nargs='?', choices=["movie", "tv"], default='tv', help='Can be set to tv or movie.')
parser.add_argument('query', help='Search query')
parser.add_argument('latest', nargs='?', default='0', help='If set to latest, the latest episode will play.')
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


def show(q):
    url = 'https://eztv.ag/search/' + q
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    magnets = soup.find_all('a', {'class': 'magnet'}, href=True)

    if magnets is None:
        sys.exit('No results found')

    arr, count = [], 1
    for magnet in magnets:
        arr.append({'id': count, 'title': magnet['title'][:-12], 'magnet': magnet['href']})
        count += 1

    return arr


def movie(q):
    req = requests.get('https://yts.ag/api/v2/list_movies.json?query_term=%s&sort_by=seeds&limit=50' % q)
    if req.status_code == 200:
        req = req.json()
        if req['status'] == 'ok':
            if req['data']['movie_count'] > 0:
                arr, count = [], 1
                for r in req['data']['movies']:
                    title = '%s (%s) (%s)' % (r['title'], r['year'], r['torrents'][0]['quality'])
                    arr.append({'id': count, 'title': title, 'magnet': r['torrents'][0]['url']})
                    count += 1
                return arr


def main():
    query = args.query

    results = []

    if args.media_type == 'tv':
        results = show(query.replace(' ', '-').lower())

    elif args.media_type == 'movie':
        results = movie(quote_plus(query))

    if args.latest == "latest":
        latest = results[0]
        print 'Playing %s!' % latest['title']
        subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --mpv' % latest['magnet']])

    else:

        if results is not None:
            print Color.BOLD + 'Enter quit to close the program.' + Color.ENDC
            print '%sSelect TV Show: %s' % (
            Color.OKBLUE, Color.ENDC) if args.media_type == 'tv' else '%s Select Movie: %s' % (
            Color.OKBLUE, Color.ENDC)
            for result in results:
                print '%s| %s |%s %s%s%s' % (
                    Color.BOLD, result['id'], Color.ENDC, Color.OKGREEN, result['title'], Color.ENDC)
        else:
            sys.exit('%s%s%s' + Color.FAIL + 'No movie results found.' + Color.ENDC)

        while True:
            read = raw_input()

            if read == 'quit':
                sys.exit()

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
                        print 'Playing %s!' % result['title']
                        subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --mpv' % result['magnet']])
            else:
                sys.exit(Color.FAIL + 'No movie results found.' + Color.ENDC)

            if not found:
                print Color.FAIL + 'Invalid selection.' + Color.ENDC


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

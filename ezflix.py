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
    req = requests.get('https://yts.ag/api/v2/list_movies.json?query_term=%s' % q)
    if req.status_code == 200:
        req = req.json()
        if req['status'] == 'ok':
            if req['data']['movie_count'] > 0:
                arr, count = [], 1
                for r in req['data']['movies']:
                    arr.append({'id': count, 'title': r['title'], 'magnet': r['torrents'][0]['url']})
                    count += 1
                return arr


if __name__ == '__main__':

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
            for result in results:
                print '| %s | %s' % (result['id'], result['title'])
            print 'Select TV Show:' if args.media_type == 'tv' else 'Select Movie:'
        else:
            sys.exit('No movie results found.')

        while True:
            read = raw_input()

            try:
                val = int(read)
            except ValueError:
                print('Expected int.')
                continue

            found = False

            if results is not None:
                for result in results:
                    if result['id'] == int(read):
                        found = True
                        print 'Playing %s!' % result['title']
                        subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --mpv' % result['magnet']])
            else:
                sys.exit('No movie results found.')

            if not found:
                print 'Invalid selection.'

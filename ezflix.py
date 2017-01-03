import subprocess
import argparse
from bs4 import BeautifulSoup
import requests
import sys
from urllib import quote_plus

parser = argparse.ArgumentParser()
parser.add_argument('media_type')
parser.add_argument('query')
parser.add_argument('latest', nargs='?', default='0')
args = parser.parse_args()


def show(q):
    url = 'https://eztv.ag/search/' + q
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    magnets = soup.find_all('a', {'class': 'magnet'}, href=True)

    if magnets is None:
        sys.exit('No results found')

    arr = []
    c = 1
    for magnet in magnets:
        arr.append({'id': c, 'title': magnet['title'][:-12], 'magnet': magnet['href']})
        c += 1

    return arr


def movie(q):
    request = requests.get('https://yts.ag/api/v2/list_movies.json?query_term=%s' % q)
    if request.status_code == 200:
        arr = request.json()
        if arr['status'] == 'ok':
            if arr['data']['movie_count'] > 0:
                l = []
                c = 1
                for r in arr['data']['movies']:
                    l.append({'id': c, 'title': r['title'], 'magnet': r['torrents'][0]['url']})
                    c += 1
                return l


if __name__ == '__main__':

    query = args.query

    results = []

    if args.media_type == 'tv':
        results = show(query.replace(' ', '-').lower())

    elif args.media_type == 'movie':
        results = movie(quote_plus(query))

    else:
        sys.exit('Incorrect media type.')

    if args.latest == "latest":
        latest = results[0]
        print 'Playing %s!' % latest['title']
        subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --mpv' % latest['magnet']])

    else:

        for result in results:
            print '| %s | %s' % (result['id'], result['title'])

        print 'Select TV Show:' if args.media_type == 'tv' else 'Select Movie:'

        while True:
            read = raw_input()

            try:
                val = int(read)
            except ValueError:
                print('Expected int.')
                continue

            found = False

            for result in results:
                if result['id'] == int(read):
                    found = True
                    print 'Playing %s!' % result['title']
                    subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --mpv' % result['magnet']])

            if not found:
                print 'Not found'

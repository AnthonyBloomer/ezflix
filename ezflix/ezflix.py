import argparse
from bs4 import BeautifulSoup
import requests
import sys
import subprocess
import re

try:
    from urllib import quote_plus
except:
    from urllib import parse

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


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def search1337(query, count=1):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    base = 'http://1337x.to'
    url = '%s/sort-category-search/%s/Movies/seeders/desc/1/' % (base, query)
    req = requests.get(url, headers=headers)
    torrents, count = [], count
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
        if re.search('/torrent/', link['href']):
            url = base + link['href']
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            title = soup.find('div', {'class', 'box-info-heading'})
            title = title.find('h1')
            rows = soup.find('ul', {'class': 'download-links'})
            magnet = rows.find('a', {'class': 'btn-magnet'})
            torrents.append({'id': count, 'title': title.text.strip(), 'magnet': magnet['href'].strip()})
            count += 1
    return torrents


def eztv(q):
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


def yts(q):
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


def main(q=None, mt=None):
    query = args.query if q is None else q
    mt = args.media_type if mt is None else mt
    player = 'mpv'

    if not cmd_exists("mpv"):
        print 'MPV not found. Defaulting to vlc.'
        player = 'vlc'

    results = []

    if mt == 'tv':
        results = eztv(query.replace(' ', '-').lower())

    elif mt == 'movie':

        try:
            results = search1337(quote_plus(query))
        except:
            results = search1337(parse.quote_plus(query))

    if args.latest == "latest":
        latest = results[0]
        print('Playing %s!' % latest['title'])
        subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --%s' % (latest['magnet'], player)])

    else:
        if results:
            print('Select TV Show:' if mt == 'tv' else 'Select Movie:')
            for result in results:
                print ('%s| %s |%s %s%s%s' % (
                    Color.BOLD, result['id'], Color.ENDC, Color.OKBLUE, result['title'], Color.ENDC))
        else:
            sys.exit('%s%s%s' % (Color.FAIL, 'No movie results found.', Color.ENDC))

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
                        print('Playing %s!' % result['title'])
                        subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --%s' % (result['magnet'], player)])
            else:
                sys.exit(Color.FAIL + 'No movie results found.' + Color.ENDC)

            if not found:
                print(Color.FAIL + 'Invalid selection.' + Color.ENDC)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

import argparse
import subprocess
import re

try:
    from urllib import quote_plus
except:
    from urllib import parse
import requests
from bs4 import BeautifulSoup
import sys

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


class Category(object):
    MOVIE = 'Movies'
    TV = 'TV'
    MUSIC = 'Music'


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def peerflix(title, magnet, player, mt):
    is_audio = '-a' if mt == 'music' else ''
    print('Playing %s!' % title)
    subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" %s --%s' % (magnet, is_audio, player)])


def eztv(q, mt=None):
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


def xtorrent(query, category):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    base = 'http://1337x.to'
    category = Category.MOVIE if category == 'movie' else Category.MUSIC
    url = '%s/category-search/%s/%s/1/' % (base, query, category)
    req = requests.get(url, headers=headers)
    torrents, count = [], 1
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all('a', href=True)
    for script in soup(["script", "style"]):
        script.extract()
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

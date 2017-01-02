from bs4 import BeautifulSoup
import requests
import subprocess
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('query')
parser.add_argument('latest', nargs='?', default='0')

args = parser.parse_args()

query = args.query.replace(' ', '-').lower()
url = 'https://eztv.ag/search/' + query

req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')

if __name__ == '__main__':
    magnets = soup.find_all('a', {'class': 'magnet'}, href=True)

    if magnets is None:
        sys.exit('No results found')
    
    results = []
    id = 1
    for magnet in magnets:
        results.append({'id': id, 'title': magnet['title'][:-12], 'magnet': magnet['href']})
        id += 1

    if args.latest == "latest":
        latest = results[0]
        print 'Playing %s!' % latest['title']
        subprocess.Popen(['/bin/bash', '-c', 'peerflix "%s" --mpv' % latest['magnet']])

    else:
        for result in results:
            print '%s %s' % (result['id'], result['title'])

        print 'Select TV show:'

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

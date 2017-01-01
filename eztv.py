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

results = []
i = 1
if __name__ == '__main__':
    print 'Searching...'

    for magnets in soup.find_all('a', {'class': 'magnet'}, href=True):
        if magnets is None:
            sys.exit('No results found')
        results.append({'id': i, 'title': magnets['title'], 'magnet': magnets['href']})
        i += 1

    if args.latest == "latest":
        latest = results[0]
        print 'Playing %s!' % latest['title']
        command = 'peerflix "%s" --mpv' % latest['magnet']
        subprocess.Popen(['/bin/bash', '-c', command])

    else:

        print 'Results:'

        for result in results:
            print '%s %s' % (result['id'], result['title'])

        print 'Select episode:'
        
        while True:
            read = input()
            for result in results:
                if result['id'] == read:
                    print 'Playing %s!' % result['title']
                    command = 'peerflix "%s" --mpv' % result['magnet']
                    subprocess.Popen(['/bin/bash', '-c', command])

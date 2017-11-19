import requests
from bs4 import BeautifulSoup
import sys


def eztv(q, limit, quality=None):
    limit = int(limit)
    url = 'https://eztv.ag/search/' + q
    req = requests.get(url)

    if not req.ok:
        return

    soup = BeautifulSoup(req.text, 'html.parser')
    magnets = soup.find_all('a', {'class': 'magnet'}, href=True)

    if magnets is None:
        sys.exit('No results found')

    arr, count = [], 1
    for magnet in magnets:

        if count == limit + 1:
            break

        if q.lower().strip()[0] in magnet['title'].lower():
            if quality is not None:
                if quality in magnet['title']:
                    arr.append({'id': count, 'title': magnet['title'][:-12], 'magnet': magnet['href']})
                    count += 1
            else:
                arr.append({'id': count, 'title': magnet['title'][:-12], 'magnet': magnet['href']})
                count += 1

    return arr

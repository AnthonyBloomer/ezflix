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
            seeds = magnet.find_parent().find_parent().find("font").get_text() # verified for the edge cases
            peers = "-" # as eztv doesn't give any peers detail, atleast not on the search page.
            if quality is not None:
                if quality in magnet['title']:
                    arr.append({'id': count, 'title': magnet['title'][:-12], 'magnet': magnet['href'], 'seeds': seeds, 'peers': peers})
                    count += 1
            else:
                arr.append({'id': count, 'title': magnet['title'][:-12], 'magnet': magnet['href'], 'seeds': seeds, 'peers': peers})
                count += 1

    return arr

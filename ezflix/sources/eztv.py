import requests
from bs4 import BeautifulSoup
import sys


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

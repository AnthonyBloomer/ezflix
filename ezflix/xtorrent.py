import requests
from bs4 import BeautifulSoup
import re


class Category(object):
    MOVIE = 'Movies'
    TV = 'TV'
    MUSIC = 'Music'


def xtorrent(query, category):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    base = 'http://1337x.to'

    if category == 'movie':
        category = Category.MOVIE
    elif category == 'tv':
        category = Category.TV
    else:
        category = Category.MUSIC

    url = '%s/category-search/%s/%s/1/' % (base, query, category)
    req = requests.get(url, headers=headers)
    torrents, count = [], 1
    soup = BeautifulSoup(req.text, 'html.parser')

    links = soup.find_all('a', href=True)

    for link in links:
        if re.search('/torrent/', link['href']):

            url = base + link['href']
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            title = soup.find('div', {'class', 'box-info-heading'})
            title = title.find('h1')
            rows = soup.find('ul', {'class': 'download-links'})
            magnet = rows.find('a', {'class': 'btn-magnet'})
            torrents.append({'id': count, 'title': title.text.strip(), 'magnet': magnet['href'].strip()})
            count += 1
    return torrents

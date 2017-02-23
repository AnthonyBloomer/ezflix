import requests
from bs4 import BeautifulSoup
import re


class Category(object):
    MOVIE = 'Movies'
    TV = 'TV'
    MUSIC = 'Music'


class XTorrent(object):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    base = 'http://1337x.to'

    def __init__(self, query, category):
        self.query = query
        self.category = category
        self.torrents = []
        if self.category == 'movie':
            self.category = Category.MOVIE
        elif category == 'tv':
            self.category = Category.TV
        else:
            self.category = Category.MUSIC

    def get_magnet(self, torrent_id):
        for torrent in self.torrents:
            if torrent['id'] == torrent_id:
                url = self.base + torrent['href']
                soup = self._call(url)
                title = soup.find('div', {'class', 'box-info-heading'})
                title = title.find('h1')
                rows = soup.find('ul', {'class': 'download-links'})
                magnet = rows.find('a', {'class': 'btn-magnet'})
                magnet = [title.text.strip(), magnet['href'].strip()]
                return magnet

        return False

    def get_torrents(self):
        url = '%s/category-search/%s/%s/1/' % (self.base, self.query, self.category)
        soup = self._call(url)
        links = soup.find_all('a', href=True)
        count = 1

        for link in links:
            if re.search('/torrent/', link['href']):
                self.torrents.append({
                    'id': count,
                    'title': link.text,
                    'href': link['href']
                })
                count += 1

        return self.torrents

    def _call(self, url):
        req = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        return soup

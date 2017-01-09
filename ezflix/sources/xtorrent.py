import requests
from bs4 import BeautifulSoup
import re


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

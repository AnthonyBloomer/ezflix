import requests
from bs4 import BeautifulSoup


def extratorrent(q):
    req = requests.get('http://extratorrent.cc/search/?new=1&search=%s&s_cat=4' % q)
    soup = BeautifulSoup(req.text, 'html.parser')
    table = soup.find('table', {'class', 'tl'})
    print table

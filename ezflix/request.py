import requests


class Request:

    def __init__(self, verbose=False):
        self._headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        self._verbose = verbose
        self._timeout = 30

    def get(self, url, params=None):
        req = requests.get(url, headers=self._headers, params=params)

        if not req.ok:
            req.raise_for_status()

        return req

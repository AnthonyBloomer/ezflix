import requests
import pprint
from tmdbv3api import TMDb, TV


def eztv(q, limit, quality=None):
    tmdb = TMDb()
    tmdb.api_key = 'e1076b74406e0a7d0efb5318f1b662d0'
    tv = TV()
    search = tv.search(q)
    if not search:
        return
    details = tv.external_ids(search[0].id)
    req = requests.get('https://eztv.ag/api/get-torrents?imdb_id=%s' % details['imdb_id'][2:])
    if not req.ok:
        return
    results, count = [], 1
    search_results = req.json()
    if 'torrents' not in search_results:
        return

    for result in search_results['torrents']:
        obj = {'id': count,
               'title': result['title'],
               'magnet': result['magnet_url'],
               'seeds': result['seeds'],
               'peers': result['peers'],
               'release_date': result['date_released_unix']
               }
        results.append(obj)
        count += 1
    return results


if __name__ == '__main__':
    pprint.pprint(eztv('The Sinner', 20))

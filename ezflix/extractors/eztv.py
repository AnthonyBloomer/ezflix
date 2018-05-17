import requests
import pprint
import datetime
from tmdbv3api import TMDb, TV


def eztv(q, limit, page=1, quality=None):
    tmdb = TMDb()
    tmdb.api_key = 'e1076b74406e0a7d0efb5318f1b662d0'
    tv = TV()
    search = tv.search(q)
    if not search:
        return
    url = 'https://eztv.ag/api/get-torrents'
    details = tv.external_ids(search[0].id)
    req = requests.get('%s?imdb_id=%s&page=%s&limit=%s' % (url, details['imdb_id'][2:], page, limit))
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
               'release_date': datetime.datetime.fromtimestamp(int(result['date_released_unix'])).strftime('%Y-%m-%d %H:%M:%S')
               }
        if quality is not None:
            if quality.lower() in result['title']:
                results.append(obj)
                count += 1
        else:
            results.append(obj)
            count += 1
    return results


if __name__ == '__main__':
    pprint.pprint(eztv('The Sinner', 20))

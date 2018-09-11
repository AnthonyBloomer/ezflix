import requests
import pprint
import colorful
from datetime import datetime
from tmdbv3api import TMDb, TV
from prettytable import PrettyTable


def select_show(search_results):
    count = 1
    row = PrettyTable()
    row.field_names = ["Id", "TV Title"]
    row.align = 'l'
    for result in search_results:
        row.add_row([count, result.name])
        count += 1
    print(row)
    while True:
        try:
            read = input()
            int_val = int(read)
            if not int_val > 0 or len(search_results) < int_val:
                print(colorful.red('Invalid selection.'))
                continue
            else:
                break
        except Exception as e:
            print(colorful.red('Invalid selection.'))
            continue


def eztv(q, limit, page=1, quality=None):
    tmdb = TMDb()
    tmdb.api_key = 'e1076b74406e0a7d0efb5318f1b662d0'
    tv = TV()
    sr = tv.search(q)
    if not sr:
        return
    url = 'https://eztv.ag/api/get-torrents'
    details = tv.external_ids(sr[0].id)
    req = requests.get('%s?imdb_id=%s&page=%s&limit=%s' % (url, details['imdb_id'][2:], page, limit))
    if not req.ok:
        return
    results, count = [], 1
    search_results = req.json()
    if 'torrents' not in search_results:
        return
    for result in search_results['torrents']:
        obj = {
            'id': count,
            'title': result['title'],
            'magnet': result['magnet_url'],
            'seeds': result['seeds'],
            'peers': result['peers'],
            'release_date': datetime.fromtimestamp(int(result['date_released_unix'])).strftime('%Y-%m-%d %H:%M:%S')
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

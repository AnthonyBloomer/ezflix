import requests


def yts(query_term, quality=None, limit=20, minimum_rating=4, sort_by='seeds', sort_order='desc'):
    params = {
        'query_term': query_term,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'limit': limit,
        'quality': quality,
        'minimum_rating': minimum_rating

    }
    req = requests.get('https://yts.ag/api/v2/list_movies.json', params=params)

    if not req.ok:
        return

    req = req.json()

    if not req['status'] == 'ok' or not req['data']['movie_count'] > 0:
        return

    arr, count = [], 1
    for r in req['data']['movies']:
        if 'torrents' in r:
            for torrent in r['torrents']:
                title = '%s (%s) (%s)' % (r['title'], r['year'], torrent['quality'])
                if quality is not None and quality == torrent['quality']:
                        arr.append({'id': count, 'title': title, 'magnet': torrent['url'], 'seeds': torrent['seeds'], 'peers': torrent['peers']})
                        count += 1
                else:
                    arr.append({'id': count, 'title': title, 'magnet': torrent['url'], 'seeds': torrent['seeds'], 'peers': torrent['peers']})
                    count += 1
    return arr

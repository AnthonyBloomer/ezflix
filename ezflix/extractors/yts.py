import requests


def yts(q, quality=None, limit=20, minimum_rating=4, sort_by='seeds', sort_order='desc'):
    params = {
        'query_term': q,
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
        for torrent in r['torrents']:

            if quality is not None:
                if quality == torrent['quality']:
                    title = '%s (%s) (%s)' % (r['title'], r['year'], torrent['quality'])
                    arr.append({'id': count, 'title': title, 'magnet': torrent['url']})
                    count += 1
            else:
                title = '%s (%s) (%s)' % (r['title'], r['year'], torrent['quality'])
                arr.append({'id': count, 'title': title, 'magnet': torrent['url']})
                count += 1
    return arr

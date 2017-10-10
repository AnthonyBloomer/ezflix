import requests


def yts(q, limit=20, minimum_rating=4, quality='720p', sort_by='seeds', sort_order='desc'):
    params = {
        'query_term': q,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'limit': limit,
        'quality': quality,
        'minimum_rating': minimum_rating

    }
    req = requests.get('https://yts.ag/api/v2/list_movies.json', params=params)

    if req.status_code == 200:
        req = req.json()
        if req['status'] == 'ok':
            if req['data']['movie_count'] > 0:
                arr, count = [], 1
                for r in req['data']['movies']:
                    for torrent in r['torrents']:
                        title = '%s (%s) (%s)' % (r['title'], r['year'], torrent['quality'])
                        arr.append({'id': count,
                                    'title': title,
                                    'magnet': torrent['url']})
                        count += 1
                return arr

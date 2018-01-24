from ezflix.request import Request
from datetime import datetime

def yts(query_term, quality=None, limit=20, minimum_rating=4, sort_by='date_added', sort_order='asc', page=1):
    params = {
        'query_term': query_term,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'limit': limit,
        'quality': quality,
        'minimum_rating': minimum_rating,
        'page': page

    }
    r = Request()
    req = r.get('https://yts.ag/api/v2/list_movies.json', params=params)
    req = req.json()
    if 'movies' not in req['data'] or not req['status'] == 'ok' or not req['data']['movie_count'] > 0:
        return
    arr, count = [], 1
    for r in req['data']['movies']:
        if 'torrents' in r:
            for torrent in r['torrents']:
                title = '%s (%s) (%s)' % (r['title'], r['year'], torrent['quality'])
                obj = {'id': count,
                       'title': title,
                       'magnet': torrent['url'],
                       'seeds': torrent['seeds'],
                       'peers': torrent['peers'],
                       'release_date': datetime.strptime(torrent['date_uploaded'], '%Y-%m-%d %H:%M:%S').date()}
                if quality is not None:
                    if quality == torrent['quality']:
                        arr.append(obj)
                        count += 1
                else:
                    arr.append(obj)
                    count += 1
    return arr[0:limit]

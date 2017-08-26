import requests


def yts(q, limit=20):
    req = requests.get('https://yts.ag/api/v2/list_movies.json?query_term=%s&sort_by=seeds&limit=%s' % (q, limit))
    if req.status_code == 200:
        req = req.json()
        if req['status'] == 'ok':
            if req['data']['movie_count'] > 0:
                arr, count = [], 1
                for r in req['data']['movies']:
                    title = '%s (%s) (%s)' % (r['title'], r['year'], r['torrents'][0]['quality'])
                    arr.append({'id': count, 'title': title, 'magnet': r['torrents'][0]['url']})
                    count += 1

                    if count == limit + 1:
                        break
                return arr

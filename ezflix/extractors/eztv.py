import requests
from datetime import datetime
from tmdbv3api import TMDb, TV
from pprint import pprint
from ezflix.torrent import Torrent

tmdb = TMDb()
tmdb.api_key = "e1076b74406e0a7d0efb5318f1b662d0"
URL = "https://eztv.io/api/get-torrents"


def search_tmdb_shows(q):
    tv = TV()
    sr = tv.search(q)
    return sr


def get_external_id(show_id):
    tv = TV()
    details = tv.external_ids(show_id)
    return details["imdb_id"] if "imdb_id" in details else None


def eztv(q, limit, page=1, quality=None, debug=False):
    sr = search_tmdb_shows(q)
    if not sr:
        return
    overview = sr[0].overview
    imdb_id = get_external_id(sr[0].id)
    if imdb_id:
        imdb_id = imdb_id[2:]
        req = requests.get(
            "%s?imdb_id=%s&page=%s&limit=%s" % (URL, imdb_id, page, limit)
        )
        if debug:
            print(req.status_code)
        results, count = [], 1
        search_results = req.json()
        if debug:
            pprint(search_results)
        if "torrents" in search_results:
            for result in search_results["torrents"]:
                release_date = datetime.fromtimestamp(int(result["date_released_unix"]))
                torrent = Torrent(
                    count,
                    result["title"],
                    result["magnet_url"],
                    result["seeds"],
                    result["peers"],
                    overview,
                    "-",
                    imdb_id,
                    release_date,
                    genre="-",
                )
                torrent_dict = torrent.build()
                if quality is not None:
                    if quality.lower() in result["title"]:
                        results.append(torrent_dict)
                        count += 1
                else:
                    results.append(torrent_dict)
                    count += 1
        if debug:
            pprint(results)
        return results

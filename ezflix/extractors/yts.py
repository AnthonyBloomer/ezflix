import requests
from pprint import pprint
from ezflix.torrent import Torrent

URL = "https://yts.mx/api/v2"


def _build_obj(req, quality, limit):
    if (
        "movies" not in req["data"]
        or not req["status"] == "ok"
        or not req["data"]["movie_count"] > 0
    ):
        return
    arr, count = [], 1
    for r in req["data"]["movies"]:
        if "torrents" in r:
            for torrent in r["torrents"]:
                title = "%s (%s) (%s)" % (r["title"], r["year"], torrent["quality"])
                release_date = torrent["date_uploaded"]
                info = Torrent(
                    count,
                    title,
                    torrent["url"],
                    torrent["seeds"],
                    torrent["peers"],
                    r["synopsis"],
                    r["rating"],
                    r["imdb_code"],
                    release_date,
                    trailer=r["yt_trailer_code"],
                    yts_id=r["id"],
                    genre=r["genres"][0],
                )
                torrent_dict = info.build()
                if quality is not None:
                    if quality == torrent["quality"]:
                        arr.append(torrent_dict)
                        count += 1
                else:
                    arr.append(torrent_dict)
                    count += 1

    return arr[0:limit]


def find_similar(movie_id, quality=None, limit=20, debug=False):
    return make_request(
        "%s/movie_suggestions.json" % URL, quality, limit, {"movie_id": movie_id}, debug
    )


def yts(
    q,
    quality=None,
    limit=20,
    minimum_rating=4,
    sort_by="date_added",
    sort_order="asc",
    page=1,
    debug=False,
):
    params = {
        "query_term": q,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "limit": limit,
        "quality": quality,
        "minimum_rating": minimum_rating,
        "page": page,
    }
    return make_request("%s/list_movies.json" % URL, quality, limit, params, debug)


def make_request(url, quality, limit, params, debug):
    req = requests.get(url, params=params)
    req = req.json()
    if debug:
        pprint(req)
    return _build_obj(req, quality, limit)

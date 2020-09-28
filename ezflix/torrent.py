class Torrent:
    def __init__(
        self,
        torrent_id,
        title,
        link,
        seeds,
        peers,
        overview,
        rating,
        imdb,
        release_date,
        **kwargs
    ):
        self.torrent_id = torrent_id
        self.title = title
        self.link = link
        self.seeds = seeds
        self.peers = peers
        self.overview = overview
        self.rating = rating
        self.imdb = imdb
        self.release_date = release_date
        self.kwargs = kwargs

    def build(self):
        base = {
            "id": self.torrent_id,
            "title": self.title,
            "link": self.link,
            "seeds": self.seeds,
            "peers": self.peers,
            "overview": self.overview,
            "rating": self.rating,
            "imdb": self.imdb,
            "release_date": self.release_date,
        }

        torrent = base.copy()
        torrent.update(self.kwargs)
        return torrent

# ezflix

Command line utility to search for TV shows and movie torrents and stream using Peerflix automatically.

### Install 

Clone the repo, then run: 

```
pip install -r requirements.txt
```

This program requires [Peerflix](https://github.com/mafintosh/peerflix). You can install Peerflix via NPM.

```
npm install -g peerflix
```

### Usage

Run ```python ezflix.py [tv/movie] [query]``` then from the list, select the torrent you want to stream. 

### Examples

```bash
python ezflix.py tv "The Man in the High Castle"
```

You can also pass an optional argument "latest" to watch the latest episode of a given TV series. For example:

```bash
python ezflix.py tv "South Park" latest
```

To search for movies, pass the "movie" argument. For example:

```bash
python ezflix.py movie "Mad Max"
```

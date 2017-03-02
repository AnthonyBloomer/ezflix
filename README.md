# ezflix

Command line utility to search for TV shows and movie torrents and stream using Peerflix automatically.

### Install 

```
pip install ezflix
```

This program requires [Peerflix](https://github.com/mafintosh/peerflix). You can install Peerflix via [NPM](https://www.npmjs.com).

```
npm install -g peerflix
```

### Usage

Run ```ezflix [tv/movie/music] [query]``` then from the list, select the torrent you want to stream. 

### Examples

```bash
ezflix tv "The Man in the High Castle"
```

You can also pass an optional argument "latest" to watch the latest episode of a given TV series.

```bash
ezflix tv "South Park" latest
```

To search for movies, pass the "movie" argument.

```bash
ezflix movie "Mad Max"
```

To search for music, pass the "music" argument.

```bash
ezflix music "Taylor Swift"
```

### Run development version

```bash
git clone https://github.com/AnthonyBloomer/ezflix.git && cd ezflix
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python setup.py install

```

# ezflix

Command line utility to search for TV shows and movie torrents and stream using Peerflix automatically.

### Install 

```
pip install -r requirements.txt
```

### Usage

Run ```python ezflix.py [query]``` then from the list, select the TV episode or movie you want to stream. 

### Examples

```bash
python ezflix.py "The Man in the High Castle"
```

You can also pass an optional argument "latest" to watch the latest episode of a given TV series. For example:

```bash
python ezflix.py "South Park" latest
```

To search for movies, pass the "movie" argument. For example:

```bash
python ezflix.py movie "Mad Max"
```

### Requires

This program requires [Peerflix](https://github.com/mafintosh/peerflix). You can install Peerflix via NPM.

```
npm install -g peerflix
```

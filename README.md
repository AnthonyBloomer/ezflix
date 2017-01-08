# ezflix

Command line utility to search for TV shows and movie torrents and stream using Peerflix automatically.

### Install 

```
pip install ezflix
```

This program requires [Peerflix](https://github.com/mafintosh/peerflix). You can install Peerflix via NPM.

```
npm install -g peerflix
```

### Usage

Run ```ezflix [tv/movie] [query]``` then from the list, select the torrent you want to stream. 

### Examples

```bash
ezflix tv "The Man in the High Castle"
```

You can also pass an optional argument "latest" to watch the latest episode of a given TV series. For example:

```bash
ezflix tv "South Park" latest
```

To search for movies, pass the "movie" argument. For example:

```bash
ezflix movie "Mad Max"
```

VLC is the default video player but if you use MPV (recommended), you can pass in an optional argument.

```bash
ezflix mpv tv "Silicon Valley" latest
```
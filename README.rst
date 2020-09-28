ezflix
======

|Build Status| |codecov|

Command line utility that enables users to search for TV and movie torrents and stream using Peerflix automatically.

Features
~~~~~~~~

- Extracts Torrent data from multiple APIs.
- Provides advanced search functionality. Filter by sort type (download count, seeds, likes), genres, minimum rating. 
- Includes subtitle support where subtitles can be downloaded automatically for the chosen TV show or movie.

Install
~~~~~~~

ezflix is available on the Python Package Index (PyPI) at https://pypi.python.org/pypi/ezflix

You can install ezflix using pip.

::

    $ pip install ezflix

This program requires Peerflix. You can install Peerflix via `npm <https://www.npmjs.com/package/peerflix>`_.

::

    $ npm install -g peerflix

    
Supported Media Players
~~~~~~~~~~~~~~~~~~~~~~~

Below is a list of media players supported in Peerflix.

- mpv
- airplay
- vlc
- mplayer
- smplayer
- mpchc
- potplayer
- webplay
- omx

In ezflix, the default player is mpv. It will fallback to vlc if mpv isn't found.

You can use the media_player argument to set your media player.

CLI Usage
~~~~~~~~~

::

    usage: ezflix [-h] [--limit [LIMIT]] [--minimum_rating [MINIMUM_RATING]]
                  [--media_player [{mpv,vlc,mplayer,smplayer,mpchc,potplayer,webplay,omx,airplay}]]
                  [--latest] [--subtitles]
                  [--sort_by [{download_count,like_count,date_added,seeds,peers,rating,title,year}]]
                  [--sort_order [{asc,desc}]] [--quality [{720p,1080p,3d}]]
                  [--genre GENRE] [--remove] [--no_seeds] [--debug] [--no-menu]
                  [--language LANGUAGE] [-v]
                  [{movie,tv}] query

    positional arguments:
      {movie,tv}            The media type.
      query                 The search query.

    optional arguments:
      -h, --help            show this help message and exit
      --limit [LIMIT]       TThe limit of results per page that has been set
      --minimum_rating [MINIMUM_RATING]
                            Used to filter movie by a given minimum IMDb rating
      --media_player [{mpv,vlc,mplayer,smplayer,mpchc,potplayer,webplay,omx,airplay}]
                            The media player.
      --latest              Play the latest TV episode.
      --subtitles           Load subtitles file.
      --sort_by [{download_count,like_count,date_added,seeds,peers,rating,title,year}]
                            Sorts the results by choosen value
      --sort_order [{asc,desc}]
                            Orders the results by either Ascending or Descending
                            order
      --quality [{720p,1080p,3d}]
                            Used to filter by a given quality.
      --genre GENRE         Used to filter by a given genre (See
                            http://www.imdb.com/genre/ for full list)
      --remove              Remove files on exit.
      --no_seeds            Include torrents that have no seeds
      --debug               Set this flag to print JSON to stdout.
      --no-menu             Set this flag to not show the usage menu on program
                            startup.
      --language LANGUAGE   Language as IETF code. Set this argument to download
                            subtitles in a given language.
      -v, --version         show program's version number and exit

Once you get the list of torrents returned, these options are available:

- Enter the id of the search result you want to stream. This will start streaming the torrent in the media player specified.
- Enter 'next' to see the next page of movies.
- Enter 'prev' to see the previous page of movies.
- Enter 'search' to refine your search.
- Enter 'info' and the id of the torrent to get the movie/tv show overview.
- Enter 'trailer' and the id of the torrent to play the movie trailer.
- Enter 'similar' and the id of the torrent to find similar movies.
- Enter 'imdb' and the id of the torrent to open the imdb media webpage.
- Enter 'quit' to close the program.

Examples
~~~~~~~~

.. code:: bash

    $ ezflix "The Man in the High Castle"

Pass '--latest' to watch the latest episode of a given TV series.

.. code:: bash

    $ ezflix "South Park" --latest

To search for movies, pass the 'movie' argument.

.. code:: bash

    $ ezflix movie "Mad Max"

Search for movies released in 2017 and order by like count descending.

.. code:: bash

    $ ezflix movie '2017' --sort_by=like_count --sort_order=desc

Search for thrillers released in 2017 and order by download count descending.

.. code:: bash

    $ ezflix movie '2017' --sort_by=download_count --sort_order=desc --genre=thriller

Automatically download German subtitles for your chosen TV show or movie. 

.. code:: bash

    $ ezflix movie 'Goodfellas' --subtitles --language=de

Pass the quality argument to only list torrents of a given quality.


.. code:: bash

    $ ezflix movie 'They Live' --quality=720p

Tests
~~~~~

The Python unittest module contains its own test discovery function, which you can run from the command line:

::

    $ python -m unittest discover tests/

Programmatic Usage
~~~~~~~~~~~~~~~~~~

You can use Ezflix programmatically in your own applications.

Search for movie torrents by title and print out the torrent link for each result.

.. code:: python

    from ezflix import Ezflix

    ezflix = Ezflix(query='Goodfellas', media_type='movie', quality='720p', limit=1)
    movies = ezflix.search()
    for movie in movies:
        print(movie['link'])

Search for tv torrents by title and print out the torrent link for each result.

.. code:: python

    from ezflix import Ezflix

    ezflix = Ezflix(query='chernobyl')
    shows = ezflix.search()
    for s in shows:
        print(s['link'])

        
Contributing
~~~~~~~~~~~~

Pull requests and feedback on how to improve this project is always welcome. 

To submit a PR:

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.

.. |Build Status| image:: https://travis-ci.org/AnthonyBloomer/ezflix.svg?branch=master
   :target: https://travis-ci.org/AnthonyBloomer/ezflix
   
.. |codecov| image:: https://codecov.io/gh/AnthonyBloomer/ezflix/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/AnthonyBloomer/ezflix
 

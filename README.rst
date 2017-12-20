ezflix
======

|Build Status| |codecov|

Command line utility that allows you to search for TV and movie torrents and
stream using Peerflix automatically. Ezflix provides advanced search capabilities including filtering by sort type (download count, seeds, likes), genres, minimum rating, etc. Ezflix also includes subtitle support where subtitles can be downloaded automatically for the chosen TV show or movie. 


|asciicast|

.. |asciicast| image:: https://asciinema.org/a/wazWQXnE8bdqXNTjshqtKIuWj.png
   :target: https://asciinema.org/a/wazWQXnE8bdqXNTjshqtKIuWj
   
Install
~~~~~~~

ezflix is available on the Python Package Index (PyPI) at https://pypi.python.org/pypi/ezflix

You can install ezflix using pip.

::

    $ pip install ezflix

This program requires Peerflix. You can install Peerflix via NPM.

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

Usage
~~~~~

::

    usage: ezflix [-h] [--limit [LIMIT]] [--minimum_rating [MINIMUM_RATING]]
              [--media_player [{mpv,vlc,mplayer,smplayer,mpchc,potplayer,webplay,omx,airplay}]]
              [--latest] [--subtitles]
              [--sort_by [{download_count,like_count,date_added,seeds,peers,rating,title,year}]]
              [--sort_order [{asc,desc}]] [--quality [{720p,1080p,3d}]]
              [--genre GENRE] [--remove] [--language LANGUAGE]
              [{movie,tv}] query

    positional arguments:
      {movie,tv}            The media type.
      query                 The search query.

    optional arguments:
      -h, --help            show this help message and exit
      --limit [LIMIT]       The number of results to return.
      --minimum_rating [MINIMUM_RATING]
                            Used to filter movie by a given minimum IMDb rating
      --media_player [{mpv,vlc,mplayer,smplayer,mpchc,potplayer,webplay,omx,airplay}]
                            The media player.
      --latest              Play the latest TV episode.
      --subtitles           Load subtitles file.
      --sort_by [{download_count,like_count,date_added,seeds,peers,rating,title,year}]
                            Use this argument to sort the torrents.
      --sort_order [{asc,desc}]
                            Use this argument to set the sort order.
      --quality [{720p,1080p,3d}]
                            Use this argument to set the min quality.
      --genre GENRE         Used to filter by a given genre (See
                            http://www.imdb.com/genre/ for full list)
      --remove              Remove files on exit.
      --language LANGUAGE   Language as IETF code. Set this argument to download
                            subtitles in a given language.

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


Run development version
~~~~~~~~~~~~~~~~~~~~~~~

Before any new changes are pushed to PyPi, you can clone the development version to avail of any new features.

.. code:: bash

    $ git clone https://github.com/AnthonyBloomer/ezflix.git
    $ cd ezflix
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py install

Tests
~~~~~

The Python unittest module contains its own test discovery function, which you can run from the command line:

::

    $ python -m unittest discover tests/

Programmatic Usage
~~~~~~~~~~~~~~~~~~

You can use Ezflix programmatically in your own applications. Consider the following example:

.. code:: python

    from ezflix import Ezflix

    ezflix = Ezflix(query="Goodfellas", media_type='movie')

    torrents = ezflix.get_torrents()
    
    if len(torrents) > 0:
        for torrent in torrents:
            print(torrent['title'])
            print(torrent['magnet'])

    
        first = torrents[0]
        file_path = ezflix.find_subtitles(first['title'])
        print(file_path)
        
Contributing
~~~~~~~~~~~~

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.

.. |Build Status| image:: https://travis-ci.org/AnthonyBloomer/ezflix.svg?branch=master
   :target: https://travis-ci.org/AnthonyBloomer/ezflix
   
.. |codecov| image:: https://codecov.io/gh/AnthonyBloomer/ezflix/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/AnthonyBloomer/ezflix

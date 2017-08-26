ezflix
======

Command line utility that allows you to search for TV and movie torrents and
stream using Peerflix automatically.

Install
~~~~~~~

ezflix is available on the Python Package Index (PyPI) at https://pypi.python.org/pypi/ezflix

You can ezflix using pip.

::

    pip install ezflix

This program requires Peerflix. You can install Peerflix via NPM.

::

    npm install -g peerflix

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

You can use the media_player flag to set your media player.

Usage
~~~~~

::

    usage: __main__.py [-h] [--limit [LIMIT]] [--media_player [MEDIA_PLAYER]]
                       [--latest] [--subtitles]
                       [--sort_by [{download_count,like_count,date_added,seeds,peers,rating,title,year}]]
                       [--sort_order [{asc,desc}]] [--quality [{720p,1080p,3d}]]
                       [{movie,tv}] query

    positional arguments:
      {movie,tv}            The media type.
      query                 The search query.

    optional arguments:
      -h, --help            show this help message and exit
      --limit [LIMIT]       The number of results to return.
      --media_player [MEDIA_PLAYER]
                            The media player.
      --latest              Play the latest TV episode.
      --subtitles           Load subtitles file.
      --sort_by [{download_count,like_count,date_added,seeds,peers,rating,title,year}]
                            Use this flag to sort the torrents.
      --sort_order [{asc,desc}]
                            Use this flag to set the sort order.
      --quality [{720p,1080p,3d}]
                            Use this flag to set the desired quality.



Please note the filtering options only work for movie torrents.

Examples
~~~~~~~~

.. code:: bash

    ezflix "The Man in the High Castle"

Pass '--latest' to watch the latest episode of a given TV series.

.. code:: bash

    ezflix "South Park" --latest

To search for movies, pass the 'movie' argument.

.. code:: bash

    ezflix movie "Mad Max"


Run development version
~~~~~~~~~~~~~~~~~~~~~~~

Before any new changes are pushed to PyPi, you can clone the development version to avail of any new features.

.. code:: bash

    git clone https://github.com/AnthonyBloomer/ezflix.git && cd ezflix
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py install



Contributing
------------

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.

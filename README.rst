ezflix
======

Command line utility that allows you to search for TV and movie torrents and
stream using Peerflix automatically.

Install
~~~~~~~

::

    pip install ezflix

This program requires Peerflix. You can install Peerflix via NPM.

::

    npm install -g peerflix

Usage
~~~~~

::

    usage: __main__.py [-h] [--limit [LIMIT]] [--media_player [MEDIA_PLAYER]]
                       [--latest]
                       [{movie,tv,music}] query

    positional arguments:
      {movie,tv,music}      The media type
      query                 The search query.

    optional arguments:
      -h, --help            show this help message and exit
      --limit [LIMIT]       The number of results to return
      --media_player [MEDIA_PLAYER]
                            The media player.
      --latest              Play the latest TV episode.



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

.. code:: bash

    git clone https://github.com/AnthonyBloomer/ezflix.git && cd ezflix
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py install


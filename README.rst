ezflix
======

Command line utility that allows you to search for TV shows and movie torrents and
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

  usage: ezflix [-h] {movie,tv,music} query [latest]

  positional arguments:
    {movie,tv,music}
    query
    latest

  optional arguments:
    -h, --help        show this help message and exit

To refine your search query, enter ``search`` then run ``media_type query`` where media_type can be movie, tv or music.

Examples
~~~~~~~~

.. code:: bash

    ezflix tv "The Man in the High Castle"

You can also pass an optional argument 'latest' to watch the latest
episode of a given TV series.

.. code:: bash

    ezflix tv "South Park" latest

To search for movies, pass the 'movie' argument.

.. code:: bash

    ezflix movie "Mad Max"

To search for music, pass the 'music' argument.

.. code:: bash

    ezflix music "Taylor Swift"

Run development version
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/AnthonyBloomer/ezflix.git && cd ezflix
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python setup.py install


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

    usage: __main__.py [-h] [--latest] [{movie,tv,music}] query

    positional arguments:
        {movie,tv,music}
        query

    optional arguments:
        -h, --help        show this help message and exit
        --latest



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


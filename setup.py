# -*- coding: utf-8 -*-

import os
import sys
from shutil import rmtree

from setuptools import setup, Command

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

here = os.path.abspath(os.path.dirname(__file__))


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name="ezflix",
    packages=["ezflix", "ezflix.extractors"],
    entry_points={
        "console_scripts": ['ezflix = ezflix.main:main']
    },
    version='1.4.1',
    keywords=['torrents', 'streaming', 'movies', 'tv', 'yify', 'eztv', 'peerflix'],
    description="Command line utility to search for TV and movie torrents and stream using Peerflix automatically.",
    long_description=long_descr,
    author="Anthony Bloomer",
    author_email="ant0@protonmail.ch",
    url="https://github.com/AnthonyBloomer/ezflix",
    install_requires=[
        'beautifulsoup4',
        'requests',
        'colorful',
        'subliminal',
        'halo',
        'PTable'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    cmdclass={
        'publish': PublishCommand,
    }
)

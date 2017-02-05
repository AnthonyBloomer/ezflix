# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="ezflix",
    packages=["ezflix"],
    entry_points={
        "console_scripts": ['ezflix = ezflix.ezflix:main']
    },
    version='0.0.5.1',
    description="Command line utility to search for TV shows and movie torrents and stream using Peerflix automatically.",
    long_description=long_descr,
    author="Anthony Bloomer",
    author_email="ant0@protonmail.ch",
    url="https://github.com/AnthonyBloomer/ezflix",
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
)

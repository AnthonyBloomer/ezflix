# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="ezflix",
    packages=["ezflix", "ezflix.extractor"],
    entry_points={
        "console_scripts": ['ezflix = ezflix.ezflix:main']
    },
    version='0.0.7',
    keywords=['torrents', 'streaming'],
    description="Command line utility to search for TV shows and movie torrents and stream using Peerflix automatically.",
    long_description=long_descr,
    author="Anthony Bloomer",
    author_email="ant0@protonmail.ch",
    url="https://github.com/AnthonyBloomer/ezflix",
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
)

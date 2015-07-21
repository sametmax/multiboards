#!/usr/bin/env python
# coding: utf-8

"""
    Main script including routing, controller and server run
"""

from __future__ import unicode_literals


import re
import os
import socket
import random
import urllib
import urlparse

import settings

import logging
import logging.handlers

from codecs import open


LOG_FILENAME = '/tmp/multiboards.log'

# Set up a specific logger with our desired output level
logger = logging.getLogger('MultiBoards')
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=3000, backupCount=5)

logger.addHandler(handler)


# set default timeout to 10 seconds for all socket
socket.setdefaulttimeout(10)


def get_favicon_url(url):
    """ Try to find a favicon url on the given page """

    page = urllib.urlopen(url)
    html = page.read(10000).decode('ascii', errors='ignore')
    pattern = r"""
                           href=(?:"|')\s*
                           (?P<favicon>[^\s'"]*favicon.ico)
                           \s*(?:"|')
                      """
    try:
        match = re.search(pattern, html, re.U|re.VERBOSE)
        favicon_url = match.groups()[0]
    except (IndexError, AttributeError):
        favicon_url = '/favicon.ico'

    parsed_url = urlparse.urlparse(url)
    url_root = "%s://%s" % (parsed_url.scheme, parsed_url.netloc)

    if url_root not in favicon_url:
        favicon_url = "%s/%s" % (url_root, favicon_url.lstrip('/'))

    return favicon_url


def get_favicon(url, retry=3):
    retry = abs(retry or 1)
    for x in range(retry - 1):
        try:
            favicon_url = get_favicon_url(url)
            return urllib.urlopen(favicon_url).read(10000)
        except:
            pass
    favicon_url = get_favicon_url(url)
    return urllib.urlopen(favicon_url).read(10000)


def random_name(use_cache=True, separator=' '):
    """ Return a random combination from a nouns and adjectives file

        Example :

        >>> random_name()
    """

    nouns_file = os.path.join(settings.ROOT_DIR, 'static/adjectives.txt')
    adjectives_file = os.path.join(settings.ROOT_DIR, 'static/nouns.txt')

    if use_cache:
        try:
            nouns = random_name._cache['nouns']
            adjectives = random_name._cache['adjectives']
        except KeyError:
            nouns = open(nouns_file, encoding='ascii').readlines()
            random_name._cache['nouns'] = nouns
            adjectives = open(adjectives_file, encoding='ascii').readlines()
            random_name._cache['adjectives'] = adjectives
    else:
            nouns = open(nouns_file).readlines()
            adjectives = open(adjectives_file).readlines()

    noun = random.choice(nouns).strip()
    adjective = random.choice(adjectives).strip()
    return "%s%s%s" % (noun, separator, adjective)

random_name._cache = {}

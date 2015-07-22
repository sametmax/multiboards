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


def fetch_url(url, bytes=10000, retry=3):
    """ Returns the bytes of the ressource at this URL"""
    retry = abs(retry or 1)
    for x in range(retry - 1):
        try:  # retry silently several time
            page = urllib.urlopen(url)
            return page.read(10000)
        except:
            pass
    # try one last time and fail loudly if needed
    page = urllib.urlopen(url)
    return page.read(10000)


def get_favicon_url(url, retry=3, try_home_page=True):
    """ Try to find a favicon url on the given page """

    parsed_url = urlparse.urlparse(url)
    url_root = "%s://%s" % (parsed_url.scheme, parsed_url.netloc)

    try:
        # try to get it using a regex on the current URL
        html = fetch_url(url, retry=retry)
        html = html.decode('ascii', errors='ignore')
        pattern = r"""
                               href=(?:"|')\s*
                               (?P<favicon>[^\s'"]*favicon.[a-zA-Z]{3,4})
                               \s*(?:"|')
                          """

        match = re.search(pattern, html, re.U|re.VERBOSE)
        favicon_url = match.groups()[0]

    except IOError:
        # this is a network error so eventually, let it crash
        if not try_home_page:
            raise
        # try with the home page, maybe this one is accessible
        favicon_url = get_favicon_url(url_root, retry=retry,
                                                       try_home_page=False)
    except (IndexError, AttributeError):
        # url is not on this page, try the home page
        if try_home_page:
            return get_favicon_url(url_root, retry=retry, try_home_page=False)

        # can't find the favicon url, default to standard url
        favicon_url = '/favicon.ico'

    # make sure to have the domain of the original website in the favicon url
    if url_root not in favicon_url:
        favicon_url = "%s/%s" % (url_root, favicon_url.lstrip('/'))

    return favicon_url


def fetch_favicon(url, retry=3):
    """ Returns the bytes of the favicon of this site """
    favicon_url = get_favicon_url(url, retry=retry)
    return fetch_url(favicon_url, retry=retry)


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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
    Main script including routing, controller and server run
"""

import os
import sys
import Image
import redis
import socket
import shutil
import json
import urllib

import settings

import logging
import logging.handlers


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


def make_thumbnail(img_path):
    """
        Create thumbnail using PIL 
    """

    format = {  "jpeg": "JPEG",
                "jpg": "JPEG",
                "png": "PNG",
                "gif": "GIF"}

    size = 60, 60
 
    ext = os.path.splitext(img_path)[1].replace('.', '')
    outfile = os.path.splitext(img_path)[0]+'t.'+ext
    if img_path != outfile:
        try:
            im = Image.open(img_path)
            im.thumbnail(size)
            im.save(outfile, format[ext])
            return True
        except IOError:
            return False

def get_imgur():
    """
        Get random picture from imgur and cache them 
    """

    con = redis.StrictRedis(settings.REDIS.get('host', 'localhost'),
                        settings.REDIS.get('port', 6379),
                        settings.REDIS.get('db', 0))
    
    imgs_thumb = con.get('imgurimagelist') or []
 

    # if we have pictures in cache, return them
    if imgs_thumb:
        return json.loads(imgs_thumb)

    # else grab some pics from imgur
    assert settings.CONTENT_FILES_ROOT is not '/'

    # clean picture dir
    try:
        shutil.rmtree(settings.CONTENT_FILES_ROOT)
        os.makedirs(settings.CONTENT_FILES_ROOT)
    except (OSError, IOError):
        pass

    # get json feed
    imgs = json.load(urllib.urlopen(settings.IMGUR['url']))

    # loop throught picture list and choose defined number of pics 
    for img in imgs['data'][:settings.IMGUR['limit']]:

        #download img to disk and make a thumbnail
        img_name = img['hash'] + img['ext']
        img_thumb = img['hash'] + 't' + img['ext']
        img_url = settings.IMGUR_PREFIX + img_name
        img_path = os.path.join(settings.CONTENT_FILES_ROOT, img_name)
        urllib.urlretrieve(img_url, img_path)

        # make a tiny thumb
        if make_thumbnail(img_path):
            imgs_thumb.append(({'url': img_url,
                                'thumb': os.path.join(settings.CONTENT_DIR, img_thumb),
                                'title': img['title']}))

    # json dump list of thumb
    imgs_thumb = json.dumps(imgs_thumb)

    # save list of pics in redis and set an expiration time
    con.set('imgurimagelist', json.dumps(imgs_thumb))
    con.expire('imgurimagelist', settings.IMGUR_EXPIRE)

    # return pics list
    return imgs_thumb

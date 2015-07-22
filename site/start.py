#!/usr/bin/env python
#  coding: utf-8

from __future__ import unicode_literals, absolute_import

"""
    Main script including routing, controller and server run
"""

import json
import urllib
import socket
import random
import uuid
import redis
import clize
import short_url
import bottle
import base64

from datetime import datetime

from bottle import route, run, view, static_file, request, HTTPError, post

import settings as _settings

from utils import random_name, fetch_favicon

from models import Custom


con = redis.StrictRedis(_settings.REDIS.get('host', 'localhost'),
                        _settings.REDIS.get('port', 6379),
                        _settings.REDIS.get('db', 0))
socket.setdefaulttimeout(10)

url_encoding = short_url.UrlEncoder('กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะเแโใไๅๆ๏๐๑๒๓๔๕๖๗๘๙๚๛')

@route('/')
@view('home')
def index():
    return dict(settings=_settings)


@route('/b/:short_url')
@view('home')
def ressources(short_url=None):
    """
        Return custom board
    """
    settings = _settings
    return locals()


@route('/randomname')
def get_random_name():
    """ Return a random name for a board """
    if request.is_ajax:
        return random_name(separator=u'-')


@post('/favicon')
def fetch_favicon_base64():
    """ Return the favicon URL from a website """
    try:
        url = request.POST['url']
    except KeyError:
        raise HTTPError(400, "You must pass a site URL")
    try:
        # return favicon as base64 url to be easily included in
        # a img tag
        favicon = fetch_favicon(url)
        return b'data:image/x-icon;base64,' + base64.b64encode(favicon)
    except (IOError):
        raise HTTPError(400, "Unable to find any favicon URL")


@route('/build')
@view('build')
def build():
    """
        Build custom board with rss feed
    """
    # generate uuid for custom board
    config_id = str(uuid.uuid4())
    settings = _settings
    return locals()


@route('/build/save', method='POST')
def save():
    """
        Save custom boards to db and return url
    """
    uid = request.POST['uuid']
    prefix_url = "http://multiboards.net/b/"
    infos = request.POST['urls'].replace('undefined', '')
    name = request.POST['name']

    if uid and request.is_ajax:
        try:
            boards = Custom.get(Custom.uuid == uid)
            boards.name = name
            boards.infos = json.dumps(infos)
            boards.save()
            return prefix_url + boards.short
        except Exception:
            boards = Custom.create(name=name,
                                   uuid=uid,
                                   infos=json.dumps(infos),
                                   short='')
            url = url_encoding.encode_url(boards.id)
            boards.short = url
            boards.save()
            return prefix_url + url


@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=_settings.STATIC_FILES_ROOT)

@route('/favicon.ico')
def server_static():
    return static_file('img/favicon.ico', root=_settings.STATIC_FILES_ROOT)


@route('/content/<filename:path>')
def server_content(filename):
    return static_file(filename, root=_settings.CONTENT_FILES_ROOT)


@post('/online/')
@post('/online/<board>')
def online(board="rootboard"):
    """
        return number of online visitor
        use redis to store IP in 10 mins session then count number of ips
    """

    # poor man stats : using ip address as unique id for each user
    user_id = request.remote_addr
    board = board.decode('utf8')
    online_user_key = "board:%s:online-users" % board

    # get timestamps that we will use as scores for the redis sorted sets
    now = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    ten_minutes_ago = now - (60 * 60 * 10)

    # add current user to count
    con.zadd(online_user_key, now, user_id)
    # remove any entry older than 10 minutes
    con.zremrangebyscore(online_user_key, 0, ten_minutes_ago)
    # get user count between now and 10 minutes ago
    count = con.zcount(online_user_key, ten_minutes_ago, now)

    # do the same with the board name so we have a number of active
    # boards
    con.zadd('boards:active', now, board)
    con.zremrangebyscore('boards:active', 0, ten_minutes_ago)

    # generate funny counter
    values = [count] + [random.randint(100, 999) for i in range(3)]
    counter = '%s,%s,%s,%s' % tuple(values)

    return counter


@route('/boards/best')
def active_boards():
    """ Return the most active boards"""
    boards = con.zrangebyscore('boards:active', 0, float('+inf'))
    boards = [b for b in boards if b != 'rootboard']
    return {'boards': boards}


@route('/json/:choice')
def ressources(choice=None):
    """
        <radios>
        return radios urls and names from settings RADIOS

        <sources>
        return sites sources to scan feed

        <news>
        return news to scan feed
    """

    if choice == 'radios':

        radios = []
        for playlist in _settings.RADIOS:
            radios.append({'name': playlist[0], 'url': playlist[1]})

        return json.dumps(radios)

    elif choice == 'sources':

        # if we have a custom board
        if request.query['short_url']:
            try:
                boards = Custom.get(Custom.id == url_encoding.decode_url(request.query['short_url']))
                boards = json.loads(boards.infos)

                # Replace default boards by custom
                for board in eval(boards):
                    bb = board.split(';')
                    try:
                        _settings.SOURCES[int(bb[0])] = ['', '', bb[1], bb[2], bb[3], bb[4]]
                    except Exception:
                        pass
            except:
                pass

        return json.dumps(_settings.SOURCES)


    elif choice == 'news':
        return json.dumps(_settings.BOTTOM_NEWS)

    elif choice == 'imgur':
        return urllib.urlopen(_settings.IMGUR).read()

    elif choice == 'bottomline':
        return _settings.BOTTOM_LINE[random.randrange(0, 5)]


@clize.clize
def start(host="127.0.0.1", port=8000, debug=True):

    if debug is not None:
        _settings.DEBUG = debug

    if _settings.DEBUG:
        bottle.debug(True)
        run(host=host, port=port, reloader=_settings.DEBUG)
    else:
        run(host=host,  port=port, server="cherrypy")


if __name__ == "__main__":
    clize.run(start)

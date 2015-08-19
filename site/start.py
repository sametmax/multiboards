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
    """ Home page """
    settings = _settings.__dict__
    settings.update({'short_url': ''})
    return locals()


@route('/b/:short_url')
@view('home')
def ressources(short_url=None):
    """
        Return custom board
    """
    settings = _settings.__dict__
    settings.update({'short_url': short_url})
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
    settings = _settings.__dict__
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
            multiboards = Custom.get(Custom.uuid == uid)
            multiboards.name = name
            multiboards.infos = json.dumps(infos)
            multiboards.save()
            return prefix_url + multiboards.short
        except Exception:
            multiboards = Custom.create(name=name,
                                        uuid=uid,
                                        infos=json.dumps(infos),
                                        short='')

            # Create short url for custom multiboards
            url = url_encoding.encode_url(multiboards.id)
            multiboards.short = url

            # Save the custom multiboards
            multiboards.save()

            # Return short url of custom multiboards
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


# @post('/online/')
# @post('/online/<board>')
# def online(board="rootboard"):
@route('/online', method='POST')
def online(board="rootboard"):
    """
        return number of online visitor
        use redis to store IP in 10 mins session then count number of ips
    """

    # poor man stats : using ip address as unique id for each user
    user_id = request.remote_addr
    # todo : fix the duplicate board name param
    board_url = request.POST.get('id', b'rootboard').decode('utf8')
    board_name = request.POST.get('name', board)
    online_user_key = "board:%s;%s:online-users" % (board_name, board_url)

    # get timestamps that we will use as scores for the redis sorted sets
    now = (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()
    ten_minutes_ago = now - (60  * 10)

    # add current user to count
    con.zadd(online_user_key, now, user_id)
    # remove any entry older than 10 minutes
    con.zremrangebyscore(online_user_key, 0, ten_minutes_ago)
    # get user count between now and 10 minutes ago
    count = con.zcount(online_user_key, ten_minutes_ago, now)

    # do the same with the board name so we have a number of active
    # boards
    con.zadd('boards:active', now, board_name)
    con.zremrangebyscore('boards:active', 0, ten_minutes_ago)

    # generate funny counter
    values = [count] + [random.randint(100, 999) for i in range(3)]
    counter = '%s,%s,%s,%s' % tuple(values)

    return counter


@route('/boards/best')
def active_boards():
    """ Return the most active boards"""
    boards = con.zrangebyscore('boards:active', 0, float('+inf'))
    boards = [b for b in boards if b.decode('utf8') != 'rootboard']
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

        # pick up radio list from setting
        # for now we are only playing ogg radios format
        radios = []
        for playlist in _settings.RADIOS:
            radios.append({'name': playlist[0], 'url': playlist[1]})

        return json.dumps(radios)



    elif choice == 'sources':

        try:
            short_url = unicode(request.query['short_url'], 'utf-8')
        except Exception, e:
            raise 'no short url'

        # if we have a custom board
        print 'short_url', short_url
        if short_url != '' and short_url != 'Multiboards':
            try:
                # init sources
                _settings.SOURCES = {}

                # get board infos
                req = Custom.get(Custom.id == url_encoding.decode_url(short_url))
                _settings.SOURCES[99] = req.name
                jsboards = json.loads(req.infos)

                # index boards
                boards = [None]*16
                for board in eval(jsboards):
                    index = board.split(';')[0].split(':')[1]
                    boards[int(index)] = board

                # Replace default boards by custom
                # ["index:0;url:http://sametmax.com/feed/;header:#ac2626;odd:#ececec;even:#f2f2f2"]
                for i in range(16):
                    if boards[i]:
                        bb = boards[i].split(';')
                        _settings.SOURCES[i] = ['', '', bb[1].split(':')[1] + ':' + bb[1].split(':')[2], bb[2].split(':')[1], bb[3].split(':')[1], bb[4].split(':')[1]]

                    else:
                        # plug the butt hole !
                        _settings.SOURCES[i] = ['', '','http://sametmax.com/feed/', 'ac2626','ececec', 'f2f2f2','', '','', '',]
                        print 'ko'

            except Exception as e:
                print e
                raise 'Et merde!'

        return json.dumps(_settings.SOURCES)

    elif choice == 'news':
        return json.dumps(_settings.BOTTOM_NEWS)

    elif choice == 'imgur':
        return urllib.urlopen(_settings.IMGUR).read()

    elif choice == 'bottomline':
        return _settings.BOTTOM_LINE[random.randrange(0, len(_settings.BOTTOM_LINE))]


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


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
    Main script including routing, controller and server run
"""

import os
import re
import json
import urllib
import socket
import random
import uuid
import redis
import clize
import short_url
import bottle

from colorweave import palette
from BeautifulSoup import BeautifulSoup
from bottle import route, run, view, static_file, request, abort

import settings as _settings

from models import Custom



con = redis.StrictRedis(_settings.REDIS.get('host', 'localhost'),
                        _settings.REDIS.get('port', 6379),
                        _settings.REDIS.get('db', 0))
socket.setdefaulttimeout(10)

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

@route('/build/colors/:site')
def colors(site=None):
    """
        Grab website dominant colors and return random matching colors
    """

    if site and request.is_ajax:

        # check if key in redis
        key = 'colors:%s' % site

        if con.get(key):
            return con.get(key)

        else:
            try:

                url = 'http://' + site

                # get site favicon url
                page = urllib.urlopen(url)
                soup = BeautifulSoup(page)
                icon_link = soup.find("link", rel=re.compile('icon'))['href']

                if icon_link == "":
                    return error
                else:
                    # Build absolute path if not exist
                    if icon_link.find('http') < 0:
                        icon_link = os.path.join(url, icon_link)

                # get favicon dominants colors and cache them for future use
                colors = [s.replace('#', '') for s in palette(url=icon_link)]
                colors.reverse()
                json_colors = json.dumps(colors)
                con.set(key, json_colors)
                con.expire(key, 3600*24*30)

                return json_colors

            except Exception, e:
                return 'error'

    return 'error'


@route('/build/save', method='POST')
def save():
    """
        Save custom boards to db and return url
    """
    uid = request.POST['uuid']
    prefix_url = "http://multiboards.net/b/"
    infos = request.POST['urls'].replace('undefined', '')

    if uid and request.is_ajax:
        try:
            boards = Custom.get(Custom.uuid == uid)
            boards.name = 'test'
            boards.infos = json.dumps(infos)
            boards.save()
            return prefix_url + boards.short
        except Exception:
            boards = Custom.create( name = 'test',
                                    uuid = uid, 
                                    infos = json.dumps(infos),
                                    short = '')
            url = short_url.encode_url(boards.id)
            boards.short = url
            boards.save()
            return prefix_url + url


@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=_settings.STATIC_FILES_ROOT)


@route('/content/<filename:path>')
def server_content(filename):
    return static_file(filename, root=_settings.CONTENT_FILES_ROOT)


@route('/online')
def online():
    """
        return number of online visitor
        use redis to store IP in 20 mins session then count number of ips
    """

    #get or create ip
    user_ip = request.remote_addr

    key = 'online-user:%s' % user_ip

    if con.get(key):
        counter = '%s,%s,%s,%s' % (len(con.keys("*online-user*")),
                                   random.randrange(100, 999),
                                   random.randrange(100, 999),
                                   random.randrange(100, 999))
        return json.dumps({'online_users': counter})
    else:
        # store ip user for 10 mins
        con.set(key, 'dummy')
        con.expire(key, 1 * 60 * 20)
        return json.dumps({'online_users': '1'})


@route('/json/:choice')
def ressources(choice=None):
    """
        <radios>
        return radios urls and names from settings RADIOS
        compatible with PLS and M3U formats

        <sources>
        return sites sources to scan feed

        <news>
        return news to scan feed
    """

    if choice == 'radios':

        radios = []

        for playlist in _settings.RADIOS:
            try:
                data = urllib.urlopen(playlist).read().split('\n')
            except:
                break

            radio_title = ''
            radio_url = ''
            for line in data:
                if line.split('=')[0] == 'File1':
                    radio_url = line.split('=')[1]
                if line.split('=')[0] == 'Title1':
                    radio_title = line.split('=')[1]
                if line.split(':')[0] == '#EXTINF':
                    radio_title = line.split('#EXTINF:')[1]
                if line[:5] == 'http:':
                    radio_url = line

            if radio_title and radio_url:
                radios.append({'title': radio_title.replace('_', ' ').title(),
                               'url': radio_url})

        return json.dumps(radios)

    elif choice == 'sources':

        # if we have a custom board
        if request.query['short_url']:
            try:
                boards = Custom.get(Custom.id == short_url.decode_url(request.query['short_url']))
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





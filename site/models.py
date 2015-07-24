#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
    Db Model to handle short urls with boards lists
"""

from peewee import *


db = SqliteDatabase('multiboards.db')


class Custom(Model):

    # Board name
    name = CharField()

    # Board array of sites urls & dominants colors
    infos = CharField()

    # Board short url
    short = CharField()

    # Board uuid
    uuid = CharField()

    class Meta:
        # this model uses the multiboards database
        database = db

# Create db if not exist
try:
    Custom.create_table()
except Exception:
    pass

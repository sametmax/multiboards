#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from __future__ import unicode_literals

######## NOT SETTINGS, JUST BOILER PLATE ##############
import os

VERSION = '0.1'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_DIR = os.path.join(ROOT_DIR, 'libs')

######## END OF BOILER PLATE ##############


# debug will get you error message and auto reload
# don't set this to True in production
DEBUG = False

# Should the application serve static files on it's own ?
# IF yes, set the absolute path to the static files.
# If no, set it to None
# In dev this is handy, in prod you probably want the HTTP servers
# to serve it, but it's OK for small traffic to set it to True in prod too.
STATIC_FILES_ROOT = os.path.join(ROOT_DIR, 'static')

# Content dir, where converted videos will be saved
CONTENT_DIR = 'content'
CONTENT_FILES_ROOT = os.path.join(ROOT_DIR, CONTENT_DIR)

# a tuple of absolute paths of directory where to look the template for
# the first one will be the first to be looked into
# if you want to override a template, create a new dir, write the
# template with the same name as the one you want to override in it
# then add the dir path at the top of this tuple
TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'views'),
)

# REDIS connections settings
REDIS = {
  'host': 'localhost',
  'port': 6379,
  'db': 0
}

# Names/links to insert in the menu bar.
# Any link with "mailto:" will be escaped to prevent spam
MENU = (
    # ('Accueil', '/', ''), # home sweet home
    # ('Contact', 'mailto:lesametlemax@gmail.com', '') # email
)

# sites to scan
# must have rss feed
SOURCES = {
     0 :[ 'sebsauvage',
          'http://sebsauvage.net/',
          'http://sebsauvage.net/links/index.php?do=rss',
          '777777',
          'ffffff',
          'f7f7f7'],
     1 :[ 'lehollandaisvolant',
          'http://lehollandaisvolant.net/',
          'http://lehollandaisvolant.net/rss.php?mode=links',
          '333333',
          'CCCCD9',
          'e3e3f3'],
     2 :[ 'korben',
          'http://korben.info/',
          'http://feeds2.feedburner.com/KorbensBlog-UpgradeYourMind',
          '41557A',
          'FFFFFF',
          'F6F6F6'],
     3 :[ 'zataz',
          'http://www.zataz.com/',
          'http://feeds.feedburner.com/ZatazNews',
          '333333',
          'F5F5F5',
          'FFFFFF'],
     4 :[ 'jeuxvideo',
          'http://www.jeuxvideo.fr/',
          'http://www.jeuxvideo.fr/xml/tout.xml',
          '013B4F',
          '85C8D9',
          'D8F1F8'],
     5 :[ 'clubic',
          'http://www.clubic.com/',
          'http://www.clubic.com/articles.rss',
          'DE302A',
          'F8F8F8',
          'FFFFFF'],
     6 :[ 'gizmodo',
          'http://www.gizmodo.fr/',
          'http://www.gizmodo.fr/feed/',
          '333333',
          'FFFFFF',
          'ECEDF1'],
     7 :[ 'reddit',
          'http://www.reddit.com/',
          'http://www.reddit.com/.rss',
          '336699',
          'EFEFEF',
          'FFFFFF'],
     8 :[ 'sametmax',
          'http://sametmax.com',
          'http://sametmax.com/feed/rss/',
          'AA2222',
          'FFFFFF',
          'E9E7E8'],
     12 :[ 'indexerror',
          'http://indexerror.net/',
          'http://indexerror.net/feed/questions.rss',
          '8AC143',
          'E7F1D9',
          'FFFFFF'],
     10 :['numerama',
          'http://www.numerama.com',
          'http://www.numerama.com/rss/news.rss',
          'B60002',
          'FFFFFF',
          'E7E7E7'],
     11 :['generation-nt',
          'http://www.generation-nt.com',
          'http://www.generation-nt.com/export/rss.xml',
          '8C2F37',
          'FFFFFF',
          'E3E9F5'],
     14 :['lesjeudis',
          'http://www.lesjeudis.com',
          'http://www.lesjeudis.com/RTQ/rss20.aspx?rssid=int_frrssljTec&num=10&chl=IL&country=FR&geoip=false&kw=Python',
          '13496A',
          'FFFFFF',
          'F4F9FD'],
     13 :['alsacreations',
          'http://alsacreations.com',
          'http://emploi.alsacreations.com/offres.xml',
          'A6C744',
          'FFFFFF',
          'EEF5F9'],
     9 :['journaldugeek',
          'http://www.journaldugeek.com',
          'http://feeds2.feedburner.com/LeJournalduGeek',
          '8C2F37',
          'FFFFFF',
          'E3E9F5'],
     15 :['humancoders',
          'http://jobs.humancoders.com',
          'http://jobs.humancoders.com/jobs.rss',
          '2D455E',
          'FFFFFF',
          'F7F7F7'],
     99 :['multiboards']
}


# bottom news
# set a bunch of news from various well knows sites
BOTTOM_NEWS = (
    ('À la une', 'http://news.google.fr/news?pz=1&cf=all&ned=fr&hl=fr&output=rss'),
    ('International', 'http://news.google.fr/news?pz=1&cf=all&ned=fr&hl=fr&topic=w&output=rss'),
    ('Économie', 'http://news.google.fr/news?pz=1&cf=all&ned=fr&hl=fr&topic=b&output=rss'),
    ('Divertissement', 'http://news.google.fr/news?pz=1&cf=all&ned=fr&hl=fr&topic=e&output=rss'),
    ('Santé', 'http://news.google.fr/news?pz=1&cf=all&ned=fr&hl=fr&topic=m&output=rss'),
    ('Science/High-Tech', 'http://news.google.fr/news?pz=1&cf=all&ned=fr&hl=fr&topic=t&output=rss')
)



# Radio playlists 
# use it from Icecast
# http://dir.xiph.org/
RADIOS = (
    ('Radio City', 'http://stream.radioreklama.bg/city.ogg'),
    ('Radio Energy','http://stream.radioreklama.bg/nrj.ogg'),
    ('Radio1 Rock','http://stream.radioreklama.bg/radio1rock.ogg'),
    ('Revolution Radio OGG','http://revolutionradio.ru/live.ogg'),
    ('Zanevskiy [MAIN] Ch.','http://178.252.126.65:8000/zanevka.ogg')
)


# imgur json feed
# can be any of the gallery page followed by json
# http://api.imgur.com/gallery
IMGUR_PREFIX = 'http://i.imgur.com/'
IMGUR_EXPIRE = 600
IMGUR = 'http://imgur.com/gallery/random.json'


# Bottom line
# display funny sentences at the bottom of the site
BOTTOM_LINE = (
    "2 + 2 = 5",
    "Si ça marche et que c'est stupide alors ce n'est pas stupide",
    "Moi aussi je me suis marié, mais j'avais une excuse : le lave-vaisselle n'existait pas encore.",
    "Il n'y a que les imbéciles qui ne changent pas d'avis ; c'est ce que j'ai toujours dit.",
    "Quand tu prends confiance en la confiance, tu deviens confiant",
    "Noël au scanner, Paques au cimetière",
    "Vous n'êtes génétiquement pas aux normes.",
    "Les femmes vivent plus longtemps que les hommes surtout quand elles sont veuves.",
    "La vraie paresse, c'est de se lever à 6 heures du matin pour avoir plus longtemps à ne rien faire.",
    "Un bon truc pour paraître dix ans plus jeune, c'est de vieillir de dix ans quand tu dis ton âge.",
    "Le ciment est composé de protons et de neutrons.",
    "Quand j'étais jeune j'étais très con. Je suis resté très jeune.",
    "Il est con comme un iceberg, trois fois plus con que ce qu'on voit !",
    "Le plus grand intellectuel du monde, même pour les courses il se fait une liste.",
    "Sur les vieilles images en noir et blanc, on voit mieux la tristesse.",
    "Un pêcheur qui se fait incinérer c'est pas tellement reconnaissant pour les asticots.",
    "La vie du bouton, elle tient qu'à un fil.",
    "La machine remplacera jamais l'homme, elle est pas assez con.",
    "L'argent que l'alcool rapporte à l'Etat, c'est énorme ; moi cette année, rien qu'en picolant, j'ai payé l'impôt sur la fortune !",
    "Y faudrait un distributeur d'apéros dans le mur pour quand ça ferme, pareil que les banques!",
    "Un SDF, tu l'assignes à résidence, il est content, le mec.",
    "C'est pas la peine d'être sans domicile fixe si c'est pour rester assis au même endroit !",
    "- Tu bois un coup ?<br>- L'autre ! Y demande à une bille si elle roule !",
    "Quarante pour cent des accidents de voiture sont provoqués par l'alcool, ça veut dire que soixante pour cent des accidents sont provoqués par des buveurs d'eau... c'est énorme !",
    "Pour un gosse, on te demande rien, alors que pour une bagnole, faut un permis !",
    "J'ai joué la date de naissance de ma femme, celle de sa mère, celle de ma fille, j'ai pas eu un seul numéro ! pas un ! c'est vraiment une famille de cons !",
    "Depuis qu'on trie les déchets, j'ai les mêmes déchets, sauf que j'ai quatorze poubelles."

)

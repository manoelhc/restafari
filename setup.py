#!/usr/bin/env python3
from distutils.core import setup
f = open('VERSION', 'r')

version = ''
for ver in f:
    version = ver


setup(
  name = 'restafari',
  packages = ['restafari'], # this must be the same as the name above
  version = version,
  description = 'Restafari is a simple REST test tool.',
  author = 'Manoel Carvalho',
  scripts = ['restafari/restafari.py'],
  author_email = 'manoelhc@gmail.com',
  url = 'https://github.com/manoelhc/restafari', # use the URL to the github repo
  download_url = 'https://github.com/manoelhc/restafari', # I'll explain this in a second
  keywords = ['testing', 'logging', 'rest', 'http', 'json'], # arbitrary keywords
  classifiers = [],
)
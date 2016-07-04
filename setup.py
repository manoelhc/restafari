#!/usr/bin/env python3
from distutils.core import setup
f = open('VERSION', 'r')

version = f.read().strip()


setup(
    name = 'restafari',
    packages = ['restafari'], # this must be the same as the name above
    license = 'MIT',
    version = version,
    description = 'Restafari is a simple REST test tool.',
    author = 'Manoel Carvalho',
    author_email = 'manoelhc@gmail.com',
    url = 'https://github.com/manoelhc/restafari', # use the URL to the github repo
    download_url = 'https://github.com/manoelhc/restafari', # I'll explain this in a second
    keywords = ['testing', 'logging', 'rest', 'http', 'json'], # arbitrary keywords
    install_requires=[
        'anyjson',
        'PyYAML',
        'ColorClass',
        'cherrypy',
        'setuptools',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    entry_points={
        'console_scripts': [
            'restafari=restafari:main',
        ],
    }
)

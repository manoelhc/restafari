#!/usr/bin/env python3
import os, os.path, cherrypy, sys


port = int(sys.argv[1].strip())

cherrypy.config.update({
  'server.socket_host': '127.0.0.1',
  'server.socket_port': port,
})

class HelloWorld(object):
  @cherrypy.expose
  def index(self):
      return "Hello world!"

if __name__ == '__main__':
  path = os.path.abspath(os.path.dirname(__file__) +'/..')
  conf = {
     '/' : {
        'tools.staticdir.root': path
     },
     '/files': {
         'tools.staticdir.on': True,
         'tools.staticdir.dir': 'outputs'
     }
  }
  cherrypy.quickstart(HelloWorld(), config=conf)

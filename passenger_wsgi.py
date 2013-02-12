import os
import sys

# append current dir and lib folder to module path
cwd = os.getcwd()
for d in ['app', 'lib', '']:
  sys.path.insert(0, os.path.join(cwd, d))

import bottle

from config import config
bottle.TEMPLATE_PATH.insert(0, config.template_path)

from app.routes import api, web, admin
from app.plugins import StripSlashesPlugin

import logging
import logging.handlers

logfilename = os.path.join(cwd, 'log', 'web.log')
log = logging.getLogger('web')
log.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler(logfilename, when='D')
log.addHandler(handler)


config.logging = log 

@bottle.error(500)
def error_handler(error):
  message = " %sURL: %s" % (error.traceback, bottle.request.url)
  log.exception(message)

def bottle_app():
  app = bottle.default_app()
  app.install(StripSlashesPlugin())
  
  return app

def application(environ, start_response):
  try:
    return bottle_app().wsgi(environ, start_response)
  except Exception, inst:
    log.exception("Error: %s", str(type(inst)))
    return []

if __name__ == "__main__":
  config.debug = True
  bottle.run(app=bottle_app(), server='cherrypy', reloader=True, debug=config.debug) 

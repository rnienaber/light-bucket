import os
import sys

# append current dir and lib folder to module path
cwd = os.getcwd()
for d in ['app', 'lib', '']:
  sys.path.insert(0, os.path.join(cwd, d))

import bottle

from config import config

bottle.TEMPLATE_PATH.insert(0, config.template_path)

from app.routes import api_routes, web_routes

import logging
logfilename = os.path.join(cwd, 'log', 'passenger_wsgi.log')
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("Running %s", sys.executable)
config.logging = logging 

def application(environ, start_response):
  try:
    return bottle.default_app().wsgi(environ, start_response)
  except Exception, inst:
    logging.exception("Error: %s", str(type(inst)))
    return []

if __name__ == "__main__":
  config.debug = True
  bottle.debug(config.debug) 
  bottle.run(reloader=config.debug) 

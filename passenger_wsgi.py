import os
import sys

# append current dir and lib folder to module path
cwd = os.getcwd()
for d in ['app', 'lib', '']:
  sys.path.insert(0, os.path.join(cwd, d))

import bottle

from config import Config
app_config = Config()

bottle.TEMPLATE_PATH.insert(0, app_config.template_path)

from app import api_routes, routes
routes.config = api_routes.config = app_config

import logging
logfilename = os.path.join(cwd, 'log', 'passenger_wsgi.log')
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("Running %s", sys.executable)
app_config.logging = logging 

def application(environ, start_response):
  try:
    return bottle.default_app().wsgi(environ, start_response)
  except Exception, inst:
    logging.exception("Error: %s", str(type(inst)))
    return []

if __name__ == "__main__":
  app_config.debug = True
  bottle.debug(app_config.debug) 
  bottle.run(reloader=True) 

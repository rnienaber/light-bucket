import os
import sys

# append current dir and lib folder to module path
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + os.sep + 'lib')

from lib import bottle
from app import routes

import logging
logfilename = os.path.join(cwd, 'passenger_wsgi.log')
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("Running %s", sys.executable)

def application(environ, start_response):
  try:
    return bottle.default_app().wsgi(environ, start_response)
  except Exception, inst:
    logging.exception("Error: %s", str(type(inst)))
    return []

if __name__ == "__main__": 
  bottle.debug(True) 
  bottle.run(reloader=True) 

import os
import sys

# append current dir to module path
cwd = os.getcwd()
sys.path.append(cwd)

from lib import bottle
from lib.bottle import route
# assuming this module is in the same dir as passenger_wsgi, this now works!

import logging
logfilename = os.path.join(cwd, 'passenger_wsgi.log')
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("Running %s", sys.executable)

@route('/')
def index():
  return "it works!"

def application(environ, start_response):
  try:
    return bottle.default_app().wsgi(environ, start_response)
  except Exception, inst:
    logging.exception("Error: %s", str(type(inst)))
    return []

if __name__ == "__main__": 
  from lib.bottle import run
  bottle.debug(True) 
  run(reloader=True) 

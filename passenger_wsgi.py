import os
import sys

# append current dir to module path
cwd = os.getcwd()
sys.path.append(cwd)

DEV_MODE = False


from lib import bottle
from lib.bottle import route, static_file
# assuming this module is in the same dir as passenger_wsgi, this now works!

import logging
logfilename = os.path.join(cwd, 'passenger_wsgi.log')
logging.basicConfig(filename=logfilename, level=logging.DEBUG)
logging.info("Running %s", sys.executable)

@route('/')
def index():
  with open('index.html', 'r') as index_file:
    return [index_file.read()]
    
@route('/<filepath:path>')
def server_static(filepath):
    public_dir = '/public' if DEV_MODE else ''
    return static_file(filepath, root=cwd + public_dir)

def application(environ, start_response):
  try:
    return bottle.default_app().wsgi(environ, start_response)
  except Exception, inst:
    logging.exception("Error: %s", str(type(inst)))
    return []

if __name__ == "__main__": 
  from lib.bottle import run
  DEV_MODE = True
  bottle.debug(True) 
  run(reloader=True) 

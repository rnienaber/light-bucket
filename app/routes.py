import os
from app.utils import render
from lib.bottle import route, static_file

WORKING_DIR = os.getcwd()
PUBLIC_DIR = os.path.join(WORKING_DIR, 'public')

@route('/')
def index():
  file_path = os.path.join(WORKING_DIR, 'index.html')
  with open(file_path, 'r') as index_file:
    return [index_file.read()]
    
@route('/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=PUBLIC_DIR)

@route('/test')
def test():
  return render('test', {'person': 'World'})
  
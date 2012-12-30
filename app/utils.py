import os
from lib import pystache

VIEW_DIR = os.path.dirname(__file__) + os.sep + 'views'

def get_all_files(file):
  cur_dir = os.path.dirname(file)
  files = [p for p in os.walk(cur_dir).next()[2] if p.endswith('.py')]
  return [os.path.splitext(f)[0] for f in files if '__init__.py' != f]
  
def render(view, model):
  view_path = os.path.join(VIEW_DIR, view + '.html') 
  with open(view_path, 'r') as view_file:
    view_contents = view_file.read()
  return [pystache.render(view_contents, model)]
import os, re
import bottle
import yaml

from bottle import jinja2_view, request

from auth import is_authenticated
from config import config

def get_all_files(file):
  cur_dir = os.path.dirname(file)
  files = [p for p in os.walk(cur_dir).next()[2] if p.endswith('.py')]
  return [os.path.splitext(f)[0] for f in files if '__init__.py' != f]
  
def get_summary(dir):
  summary_path = os.path.join(dir, 'summary.yaml')
  if not os.path.exists(summary_path):
    return {}
    
  with open(summary_path, 'r') as summary_file:
    return yaml.safe_load(summary_file)
    
def first(iterable, default=None):
  if iterable:
    for i in iterable:
      return i
  return default
  
_par_re = re.compile(r'\n{2,}')
def nl2p(text):
  if not text:
    return text
  result = u'\n'.join(u'<p>%s</p>' % p for p in _par_re.split(text))
  return result
  
def authenticated(value):
  return is_authenticated(request)
  
def view(argument, **defaults):
  template_settings = defaults.get('template_settings')
  if type(template_settings) != dict:
    template_settings = {}
    defaults['template_settings'] = template_settings
    
  template_settings.update({'filters': {'nl2p': nl2p}, 
                            'tests': {'authenticated': authenticated}})
                     
  google_analytics_key = config.settings.get('google_analytics_key')
  if google_analytics_key:
    defaults['google_analytics_key'] = google_analytics_key
  return jinja2_view(argument, **defaults)
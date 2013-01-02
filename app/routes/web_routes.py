import os
import calendar
from getimageinfo import getImageInfo
import bottle
from bottle import route, static_file, redirect
from bottle import jinja2_view as view

from utils import get_summary, clear_templates
#placeholder for config that is assigned on startup
from config import config

@route('/')
@view('index')
def index():
  clear_templates()    
  return {'summary': get_summary(config.photo_dir)}
  
@route('/<year\d{4}>/<month:re:\d{2}>/<album>/')
def album_redirect(year, month, album):
  redirect('/{0}/{1}/{2}'.format(year, month, album), 301)

@route('/<year:re:\d{4}>/<month:re:\d{2}>/<album>')
@view('album')
def album(year, month, album):
  album_dir = os.path.join(config.photo_dir, year, month, album)
  
  #TODO: add security so you can't list files using relative paths
  url_path = '/photos/{0}/{1}/{2}'.format(year, month, album)
  photos = []
  for p in os.walk(album_dir).next()[2]:
    if not p.lower().endswith(('.jpg', '.jpeg')):
      continue
      
    with open(os.path.join(album_dir, p), 'rb') as photo_file:
      data = photo_file.read(81000)
    content_type, width, height = getImageInfo(data)

    photos.append({'photo': '{0}/{1}'.format(url_path, p),
                   'width': width, 'height': height})

  clear_templates()
  return {'photos': photos,
          'year': year,
          'month_name': calendar.month_name[int(month)],
          'album_name': album.replace('_',' ').title(),
          'summary': get_summary(album_dir)}

@route('/<year:re:\d{4}>/<month:re:\d{2}>/')
def month_redirect(year, month):
  redirect('/{0}/{1}'.format(year, month), 301)
  
@route('/<year:re:\d{4}>/<month:re:\d{2}>')
@view('month')  
def month(year, month):
  month_dir = os.path.join(config.photo_dir, year, month)
  
  albums = []
  for e in os.walk(month_dir).next()[1]:
    albums.append({'title': e.replace('_', ' ').title(), 
                   'url': '/{0}/{1}/{2}'.format(year, month, e),
                   'summary': get_summary(os.path.join(month_dir, e))})

  clear_templates()
  return {'albums': albums,
          'year': year,
          'month': month,
          'month_name': calendar.month_name[int(month)],
          'summary': get_summary(month_dir)}
  
@route('/<year:re:\d{4}>/')
def year_redirect(year):
  redirect('/{0}'.format(year), 301)
  
@route('/<year:re:\d{4}>')
@view('year')  
def year(year):
  year_dir = os.path.join(config.photo_dir, year)
  
  months = []
  for m in os.walk(year_dir).next()[1]:
    months.append({'month': calendar.month_name[int(m)], 
                   'url': '/{0}/{1}'.format(year, m),
                   'summary': get_summary(os.path.join(year_dir, m))})

  clear_templates()
  return {'months': months, 'year': year,
          'summary': get_summary(year_dir)}

@route('/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=config.public_dir)

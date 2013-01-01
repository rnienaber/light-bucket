import os
import calendar
from getimageinfo import getImageInfo
import bottle
from bottle import route, static_file, redirect
from bottle import jinja2_view as view

#placeholder for config that is assigned on startup
config = ''

@route('/')
def index():
  file_path = os.path.join(config.root_dir, 'index.html')
  with open(file_path, 'r') as index_file:
    return [index_file.read()]

@route('/<year\d{4}>/<month:re:\d{2}>/<event>/')
def album_redirect(year, month, event):
  redirect('/{0}/{1}/{2}'.format(year, month, event), 301)

@route('/<year:re:\d{4}>/<month:re:\d{2}>/<event>')
@view('album')
def album(year, month, event):
  event_dir = os.path.join(config.photo_dir, year, month, event)
  
  #TODO: add security so you can't list files using relative paths
  url_path = '/photos/{0}/{1}/{2}'.format(year, month, event)
  photos = []
  for p in os.walk(event_dir).next()[2]:
    with open(os.path.join(event_dir, p), 'rb') as photo_file:
      data = photo_file.read(81000)
    content_type, width, height = getImageInfo(data)

    photos.append({'photo': '{0}/{1}'.format(url_path, p),
                   'width': width, 'height': height})

  #TODO: clears template cache for dev
  if config.debug:
    bottle.TEMPLATES.clear() 
  
  return {'photos': photos,
          'year': year,
          'month_name': calendar.month_name[int(month)],
          'event_name': event.replace('_',' ').title()}

@route('/<year:re:\d{4}>/<month:re:\d{2}>/')
def month_redirect(year, month):
  redirect('/{0}/{1}'.format(year, month), 301)
  
@route('/<year:re:\d{4}>/<month:re:\d{2}>')
@view('month')  
def month(year, month):
  month_dir = os.path.join(config.photo_dir, year, month)
  
  events = []
  for e in os.walk(month_dir).next()[1]:
    events.append({'title': e.replace('_', ' ').title(), 
                   'url': '/{0}/{1}/{2}'.format(year, month, e)})

  #TODO: clears template cache for dev
  if config.debug:
    bottle.TEMPLATES.clear()  

  return {'events': events,
          'year': year,
          'month': month,
          'month_name': calendar.month_name[int(month)]}
  
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
                   'url': '/{0}/{1}'.format(year, m)})

  #TODO: clears template cache for dev
  if config.debug:
    bottle.TEMPLATES.clear()    
  
  return {'months': months, 'year': year}

@route('/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=config.public_dir)

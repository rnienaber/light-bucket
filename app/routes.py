import os
from app.utils import render
from lib.getimageinfo import getImageInfo
from lib.bottle import route, static_file, redirect

WORKING_DIR = os.getcwd()
PUBLIC_DIR = os.path.join(WORKING_DIR, 'public')
PHOTO_DIR = os.path.join(PUBLIC_DIR, 'photos')
IMG_DIR = os.path.join(PUBLIC_DIR, 'img')

@route('/')
def index():
  file_path = os.path.join(WORKING_DIR, 'index.html')
  with open(file_path, 'r') as index_file:
    return [index_file.read()]

#work around for background images on dev
@route('/img/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=IMG_DIR)
    
@route('/<year>/<month>/<event>/')
def event_redirect(year, month, event):
  redirect('/{0}/{1}/{2}'.format(year, month, event), 301)

@route('/<year>/<month>/<event>')
def event(year, month, event):
  event_dir = os.path.join(PHOTO_DIR, year, month, event)
  
  #TODO: add security so you can't list files using relative paths
  url_path = '/photos/{0}/{1}/{2}'.format(year, month, event)
  photos = []
  for p in os.walk(event_dir).next()[2]:
    with open(os.path.join(event_dir, p), 'rb') as photo_file:
      data = photo_file.read(81000)
    content_type, width, height = getImageInfo(data)

    photos.append({'photo': '{0}/{1}'.format(url_path, p),
                   'width': width, 'height': height})

  return render('event', {'photos': photos})
    
@route('/<filepath:path>')
def server_static(filepath):
  return static_file(filepath, root=PUBLIC_DIR)
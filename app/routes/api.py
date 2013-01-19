import os
from bottle import request, response, route, post, HTTPError

from config import config

from models.album import Album
import exiftool_reader as reader
from app.auth import is_admin

@route('/<album_path:path>/metadata')
def photo_metadata(album_path):
  album = Album(path=album_path)
  response.content_type = 'application/json'
  return album.get_exif_data()

@post('/api/image/update')  
@is_admin
def update_photo_metadata():
  values = {}
  for k in request.forms.keys():
    values[k] = request.forms[k]
  
  image_path = values['image_path']
  del values['image_path']
  
  path_parts = image_path.split('/')
  reader.update_exif('/'.join(path_parts[2:]), values)
  
  Album(path=os.path.dirname(image_path)).delete_metadata_cache()
  
  
 
  
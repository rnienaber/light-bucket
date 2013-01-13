import os
from bottle import request, response, route, post, HTTPError

from config import config

from models.album import Album
import exiftool_reader as reader
from app import auth

@route('/<album_path:path>/metadata')
def photo_metadata(album_path):
  album = Album(path=album_path)
  response.content_type = 'application/json'
  return album.get_exif_data()

@post(config.photo_url_path + '/<image_path:path>/update')  
def update_photo_metadata(image_path):
  if not auth.is_authenticated(request):
    return HTTPError(404, "File does not exist.")

  
  values = {}
  for k in request.forms.keys():
    values[k] = request.forms[k]
  reader.update_exif(image_path, values)
  
  Album(path=os.path.dirname(image_path)).delete_metadata_cache()
  
  
 
  
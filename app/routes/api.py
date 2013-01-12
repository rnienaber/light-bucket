import os
from os import path
from bottle import request, response, route, post, HTTPError

from config import config

from models.album import Album
import exiftool_reader as reader
from app import auth

@route('/api/photo_metadata')
def photo_metadata():
  response.content_type = 'application/json'
  album = Album(path=request.query.path)
  return album.get_exif_data()

@post(config.photo_url_path + '/<image_path:path>/update')  
def update_photo_metadata(image_path):
  if not auth.is_authenticated(request):
    return HTTPError(404, "File does not exist.")

  values = {}
  for k in request.forms.keys():
    values[k] = request.forms[k]

  print request.forms.keys()
  reader.update_exif(image_path, values)
  
 
  
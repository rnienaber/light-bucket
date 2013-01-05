import os
from os import path
from bottle import request, response, route

from models.album import Album

@route('/api/photo_metadata')
def photo_metadata():
  response.content_type = 'application/json'
  album = Album(path=request.query.path)
  return album.get_exif_data()
 
  
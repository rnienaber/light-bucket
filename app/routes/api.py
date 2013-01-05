import os
from os import path
from bottle import request, route
from exiftool_reader import ExifToolReader

#placeholder for config that is assigned on startup
from config import config

@route('/api/photo_metadata')
def photo_metadata():
  #TODO: ensure this can't access paths below the photo_dir
  album_path = request.query.path.strip('/\\')
  full_path = path.normpath(path.join(config.photo_dir, album_path))
  paths = [path.join(album_path, p) for p in os.walk(full_path).next()[2]]
  images = [p for p in paths if p.lower().endswith(('.jpg', '.jpeg'))]
  image_relative_paths = [path.normpath(p) for p in images]
  
  return ExifToolReader(config).get_exifs(image_relative_paths)
  
  
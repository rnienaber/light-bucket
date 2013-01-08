#http://stackoverflow.com/a/273962/9539
import os
import Image

from config import config

class Thumbnail(object):
  def __init__(self, path):
    self.path = path
    
  def location(self):
    joined_path = os.path.join(config.thumbnail_dir, self.path.strip('/\\'))
    return os.path.normpath(joined_path)
    
  def photo_path(self):
    joined_path = os.path.join(config.photo_dir, self.path.strip('/\\'))
    return os.path.normpath(joined_path)
    
  def get_path(self):
    thumbnail_path = os.path.abspath(self.location())
    
    os.makedirs(os.path.dirname(thumbnail_path))
    
    im = Image.open(self.photo_path())
    im.thumbnail(config.thumbnail_size, Image.ANTIALIAS)
    im.save(thumbnail_path, "JPEG")
    
    return thumbnail_path
    
    
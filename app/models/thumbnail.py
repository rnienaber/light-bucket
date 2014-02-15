import os
from PIL import Image

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
  
  def mkdirs(self, newdir):
    '''Lovingly lifted from http://www.linux-support.com/cms/python-create-a-directory-and-its-parent-path/'''
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("cannot create directory, file already exists: '%s'" % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            self.mkdirs(head)
        if tail:
            os.mkdir(newdir)
  
  def resize(self, photo_path, thumbnail_path):
    im = Image.open(photo_path)
    wpercent = (config.thumbnail_size/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im.thumbnail((config.thumbnail_size, hsize), Image.ANTIALIAS)
    im.save(thumbnail_path, "JPEG")
  
  def get_path(self):
    thumbnail_path = os.path.abspath(self.location())
    photo_path = os.path.abspath(self.photo_path())
    if not os.path.exists(photo_path):
      return None
    if os.path.exists(thumbnail_path):
      thumbnail_time = os.path.getmtime(thumbnail_path)
      photo_time = os.path.getmtime(photo_path)
      if photo_time <= thumbnail_time:
        return thumbnail_path
    else:
      self.mkdirs(os.path.dirname(thumbnail_path))
    
    self.resize(photo_path, thumbnail_path)
    
    return thumbnail_path
    
    

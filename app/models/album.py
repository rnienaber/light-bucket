import os, re
import calendar
import simplejson as json
from getimageinfo import getImageInfo

from config import config
from utils import get_summary, first
import exiftool_reader as reader

path_regex = re.compile("(?P<year>\d{4})/(?P<month>\d+)/(?P<name>.*)")

class Album(object):
  def __init__(self, year=None, month=None, name=None, path=None):
    if not path:
      self.year = year
      self.month = month
      self.name = name
    else:
      match = path_regex.search(path)
      if not match:
        raise Exception, "Couldn't match path: '" + str(path) + "'"
      self.year, self.month, self.name = match.groups()

    #TODO: add security so you can't list files using relative paths
    self.album_dir = os.path.join(config.photo_dir, self.year, self.month, self.name)

    self.url_path = '/{0}/{1}/{2}'.format(self.year, self.month, self.name)
  
  @property
  def title(self):
    summary_title = self.summary.get('title')
    if summary_title:
      return summary_title
    else:
      return self.name.replace('_', ' ').title()

  @property
  def summary(self):
    if hasattr(self, 'cached_summary'):
      return self.cached_summary

    self.cached_summary = get_summary(self.album_dir)
    return self.cached_summary
  
  def graphic_files(self):
    for p in os.walk(self.album_dir).next()[2]:
      if p.lower().endswith(('.jpg', '.jpeg')):
        yield p
        
  def first_image_url(self):
    image_name = first(self.graphic_files())
    return self.get_thumbnail_url(image_name) if image_name else ''

  def read_image_data(self, image_name):
    with open(os.path.join(self.album_dir, image_name), 'rb') as photo_file:
      data = photo_file.read(81000)

    return getImageInfo(data)
    
  def get_image_url(self, image_name):
    return '{0}{1}/{2}'.format(config.photo_url_path, self.url_path, image_name)
    
  def get_thumbnail_url(self, image_name):
    return '{0}{1}/{2}'.format(config.thumbnail_url_path, self.url_path, image_name)
    
  def get_metadata_cache(self):
    return os.path.join(self.album_dir, config.metadata_cache_file_name)
    
  def delete_metadata_cache(self):
    cache_path = self.get_metadata_cache()
    if os.path.exists(cache_path):
      os.remove(cache_path)
    
  def get_exif_data(self):
    cache_path = self.get_metadata_cache()
    
    #check if cache exists and read it if it does
    if os.path.exists(cache_path):
      with open(cache_path, 'r') as cache_file:
        return cache_file.read()
    
    #get the exif info
    files = self.graphic_files()
    relative_paths = [os.path.join(self.url_path, p) for p in files]
    image_relative_paths = [os.path.normpath(p).strip(os.sep) for p in relative_paths]
    
    exif_info = self.run_exiftool(image_relative_paths)
    exif_data = json.dumps(exif_info)
    
    #save cache to file
    with open(cache_path, 'w') as cache_file:
      cache_file.write(exif_data)
    
    return exif_data
    
  def to_view_data(self):
    photos = []
    for p in self.graphic_files():
      content_type, width, height = self.read_image_data(p)

      photos.append({'photo': self.get_image_url(p),
                     'thumbnail': self.get_thumbnail_url(p),
                     'width': width, 'height': height})

    return {'photos': photos,
            'year': self.year,
            'month_name': calendar.month_name[int(self.month)],
            'month': self.month,
            'album': self.title,
            'name': self.name,
            'summary': self.summary}
            
  def run_exiftool(self, image_relative_paths):
    return reader.get_exifs(image_relative_paths)
    

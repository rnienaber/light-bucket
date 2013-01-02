import os
import calendar
from getimageinfo import getImageInfo
from config import config
from utils import get_summary

class Album(object):
  def __init__(self, year, month, name):
    self.year = year
    self.month = month
    self.name = name

    #TODO: add security so you can't list files using relative paths
    self.album_dir = os.path.join(config.photo_dir, year, month, name)

  def graphic_files(self):
    for p in os.walk(self.album_dir).next()[2]:
      if p.lower().endswith(('.jpg', '.jpeg')):
        yield p
        
  def read_image_data(self, image_name):
    with open(os.path.join(self.album_dir, image_name), 'rb') as photo_file:
      data = photo_file.read(81000)

    return getImageInfo(data)
    
  def to_view_data(self):
    url_path = '/photos/{0}/{1}/{2}'.format(self.year, self.month, self.name)
    photos = []
    for p in self.graphic_files():
      content_type, width, height = self.read_image_data(p)

      photos.append({'photo': '{0}/{1}'.format(url_path, p),
                     'width': width, 'height': height})

    return {'photos': photos,
            'year': self.year,
            'month': calendar.month_name[int(self.month)],
            'album': self.name.replace('_',' ').title(),
            'summary': get_summary(self.album_dir)}
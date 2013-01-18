import os
import calendar
from config import config
from utils import get_summary, first
from models.album import Album

class Month(object):
  def __init__(self, year, month):
    self.year = year
    self.month = month

    self.name = calendar.month_name[int(month)]
    self.url_path = '/{0}/{1}'.format(self.year, month)
    
    #TODO: add security so you can't list files using relative paths
    self.month_dir = os.path.join(config.photo_dir, year, month)
  
  def get_summary(self):
    return get_summary(self.month_dir)
    
  def get_albums(self):
    for e in sorted(os.walk(self.month_dir).next()[1]):
      yield Album(self.year, self.month, e)
      
  def first_image_url(self):
    album = first(self.get_albums())
    return album.first_image_url() if album else ''
    
  def to_view_data(self):
    albums = []
    for album in self.get_albums():
      albums.append({'title': album.title, 
                     'url': album.url_path,
                     'summary': album.summary,
                     'first_image_url': album.first_image_url()})

    return {'albums': albums,
            'year': self.year,
            'month': self.month,
            'month_name': self.name,
            'summary': self.get_summary()}
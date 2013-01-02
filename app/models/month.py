import os
import calendar
from config import config
from utils import get_summary

class Month(object):
  def __init__(self, year, month):
    self.year = year
    self.month = month

    #TODO: add security so you can't list files using relative paths
    self.month_dir = os.path.join(config.photo_dir, year, month)
    
  def to_view_data(self):
    albums = []
    for e in os.walk(self.month_dir).next()[1]:
      albums.append({'title': e.replace('_', ' ').title(), 
                     'url': '/{0}/{1}/{2}'.format(self.year, self.month, e),
                     'summary': get_summary(os.path.join(self.month_dir, e))})

    return {'albums': albums,
            'year': self.year,
            'month': self.month,
            'month_name': calendar.month_name[int(self.month)],
            'summary': get_summary(self.month_dir)}
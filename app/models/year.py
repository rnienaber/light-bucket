import os
import calendar
from config import config
from utils import get_summary

from models.month import Month

class Year(object):
  def __init__(self, year):
    self.year = year
    
    #TODO: add security so you can't list files using relative paths
    self.year_dir = os.path.join(config.photo_dir, year)
    
  def to_view_data(self):
    months = []
    for m in os.walk(self.year_dir).next()[1]:
      month = Month(self.year, m)
      months.append({'month': month.name, 
                     'url': month.url_path,
                     'summary': month.get_summary(),
                     'first_image_url': month.first_image_url()})

    return {'months': months, 'year': self.year,
            'summary': get_summary(self.year_dir)}
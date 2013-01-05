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

  def months(self):
    for m in os.walk(self.year_dir).next()[1]:
      yield Month(self.year, m)

  def to_view_data(self):
    months_result = []
    for m in self.months():
        months_result.append({'month': m.name,
                     'url': m.url_path,
                     'summary': m.get_summary(),
                     'first_image_url': m.first_image_url()})

    return {'months': months_result,
            'year': self.year,
            'summary': get_summary(self.year_dir)}
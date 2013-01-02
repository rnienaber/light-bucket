import os
import calendar
from config import config
from utils import get_summary

class Year(object):
  def __init__(self, year):
    self.year = year
    
    #TODO: add security so you can't list files using relative paths
    self.year_dir = os.path.join(config.photo_dir, year)
    
  def to_view_data(self):
    months = []
    for m in os.walk(self.year_dir).next()[1]:
      months.append({'month': calendar.month_name[int(m)], 
                     'url': '/{0}/{1}'.format(self.year, m),
                     'summary': get_summary(os.path.join(self.year_dir, m))})

    return {'months': months, 'year': self.year,
            'summary': get_summary(self.year_dir)}
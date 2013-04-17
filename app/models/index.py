import os
import calendar
from config import config
from utils import get_summary, first

from models.year import Year

class Index(object):
  def __init__(self):
    pass

  def to_view_data(self):
    years = []
    for y in sorted(os.walk(config.photo_dir).next()[1], reverse=True):
        year = Year(y)
        month_images = [m.first_image_url() for m in year.months()]
        image_url = first([i for i in month_images if i != ''])
        
        years.append({'view_data': year.to_view_data(),
                      'image_url': image_url})

    return {'years': years,
            'summary': get_summary(config.photo_dir)}

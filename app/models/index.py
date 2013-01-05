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
    for y in os.walk(config.photo_dir).next()[1]:
        year = Year(y)
        years.append({'view_data': year.to_view_data(),
                      'first_month_image_url': first(year.months()).first_image_url()})

    return {'years': years,
            'summary': get_summary(config.photo_dir)}
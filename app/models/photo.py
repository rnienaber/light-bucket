import re

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

FOLDER_REGEX = re.compile("(\d{4}).*(\d{2}).*\/(.+)")

Base = declarative_base()
class Photo(Base):
  __tablename__ = 'photo'
  id = Column('_id', Integer, primary_key=True)
  filename = Column(String)
  folder = Column(String)
  notes = Column(String)
  latitude = Column(Float)
  longitude = Column(Float)
  location_name = Column(String)
  people = Column(String)
  keywords = Column(String)
  timestamp = Column(DateTime)

  @property
  def normalized_folder(self):
    matches = FOLDER_REGEX.search(self.folder)
    groups = [''] + list(matches.groups())
    groups[3] = groups[3].lower().replace(' ', '_')
    return '/'.join(groups)

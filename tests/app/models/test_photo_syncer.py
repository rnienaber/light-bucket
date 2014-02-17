from os import path
import shutil

import unittest2
from app.models.photo_syncer import PhotoSyncer

from config import config

class TestPhotoSyncer(unittest2.TestCase):
  @classmethod
  def setUpClass(cls):
    database_file = path.join(config.db_dir, 'test.sqlite')
    cls.photo_syncer = PhotoSyncer(database_file, config.photo_dir)

  def photo_syncer(self):
    self.__class__.photo_syncer

  def test_should_normalize_photo_folder(self):
    photos = self.photo_syncer.all_photos()[0:4]
    
    self.assertEqual(photos[0].normalized_folder, '/2012/01/south_africa')
    self.assertEqual(photos[1].normalized_folder, '/2012/01/south_africa')
    self.assertEqual(photos[2].normalized_folder, '/2012/01/south_africa')
    self.assertEqual(photos[3].normalized_folder, '/2012/01/south_africa')

  def test_(self):
    pass
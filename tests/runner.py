import sys, os

sys.path.insert(0, os.path.abspath('../app'))
sys.path.insert(0, os.path.abspath('../lib'))
sys.path.insert(0, os.path.abspath('../'))

import unittest2 as unittest

import tests
from tests.app import models
from tests.app.test_exif_reader import TestExifReader

from config import config
current_dir = os.path.dirname(__file__)
config.photo_dir = os.path.join(current_dir, 'images')
config.thumbnail_dir = os.path.join(config.photo_dir, 'thumbnails')
config.db_dir = current_dir

if __name__ == "__main__":

  loader = unittest.TestLoader()
  all_tests = loader.discover('./app', pattern='*.py')
  # all_tests = loader.discover('./app', pattern='test_photo_syncer.py')
  unittest.TextTestRunner().run(all_tests)
  # suite = unittest.TestLoader().loadTestsFromName('tests.app.models.test_photo_syncer.TestPhotoSyncer')
  # unittest.TextTestRunner().run(suite)
  

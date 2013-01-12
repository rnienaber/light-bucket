import sys, os

sys.path.insert(0, os.path.abspath('../app'))
sys.path.insert(0, os.path.abspath('../lib'))
sys.path.insert(0, os.path.abspath('../'))

import unittest2 as unittest

import tests
from tests.app import models
from tests.app.test_exif_reader import TestExifReader

from config import config
config.photo_dir = os.path.join(os.path.dirname(__file__), 'images')
config.thumbnail_dir = os.path.join(config.photo_dir, 'thumbnails')

if __name__ == "__main__":
  loader = unittest.TestLoader()
  all_tests = loader.discover('./app', pattern='*.py')
  unittest.TextTestRunner().run(all_tests)
  #suite = unittest.TestLoader().loadTestsFromName('tests.app.test_exif_reader.TestExifReader')
  #unittest.TextTestRunner().run(suite)
  

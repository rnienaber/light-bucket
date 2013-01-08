import os, sys
import shutil
import unittest2
from getimageinfo import getImageInfo

from app.models.thumbnail import Thumbnail
from config import config

class TestThumbnail(unittest2.TestCase):
  @classmethod
  def setUpClass(cls):
    if os.path.exists(config.thumbnail_dir):
      shutil.rmtree(config.thumbnail_dir)
    os.mkdir(config.thumbnail_dir)

  @classmethod
  def tearDownClass(cls):
    if os.path.exists(config.thumbnail_dir):
      shutil.rmtree(config.thumbnail_dir)
        
  def test_should_return_thumbnail_image_if_it_exists(self):
    pass
    
  def test_thumbnail_path(self):
    thumbnail = Thumbnail('/subdir with spaces/lunch_at_dave-1.jpg')
    
    path = os.path.join(config.thumbnail_dir, 'subdir with spaces/lunch_at_dave-1.jpg')
    self.assertEquals(thumbnail.location(), os.path.normpath(path))
    
  def test_photo_path(self):
    thumbnail = Thumbnail('/subdir with spaces/lunch_at_dave-1.jpg')
    
    path = os.path.join(config.photo_dir, 'subdir with spaces/lunch_at_dave-1.jpg')
    self.assertEquals(thumbnail.photo_path(), os.path.normpath(path))
    
  def test_should_create_thumbnail_image_if_it_doesnt_exist(self):
    thumbnail = Thumbnail('subdir with spaces/lunch_at_dave-1.jpg')
    url = thumbnail.get_path()
    
    path = os.path.join(config.thumbnail_dir, 'subdir with spaces/lunch_at_dave-1.jpg')
    norm_path = os.path.normpath(path)
    self.assertTrue(os.path.exists(norm_path))

    with open(norm_path, 'rb') as photo_file:
      data = photo_file.read(81000)

    self.assertEquals(getImageInfo(data), ('image/jpeg', 200, 133))

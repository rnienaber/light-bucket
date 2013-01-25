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
    photo_path = os.path.join(config.photo_dir, 'IMG_6868.jpg')
    thumbnail_path = os.path.join(config.thumbnail_dir, 'IMG_6868.jpg')
    shutil.copy2(photo_path, thumbnail_path)
    
    thumbnail = Thumbnail('/IMG_6868.jpg')
    thumbnail_path = thumbnail.get_path()
    
    with open(thumbnail_path, 'rb') as photo_file:
      data = photo_file.read(81000)

    self.assertEquals(getImageInfo(data), ('image/jpeg', 800, 600))
    
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
    thumbnail_path = thumbnail.get_path()
    
    path = os.path.join(config.thumbnail_dir, 'subdir with spaces/lunch_at_dave-1.jpg')
    norm_path = os.path.abspath(os.path.normpath(path))

    self.assertEqual(thumbnail_path, norm_path)
    self.assertTrue(os.path.exists(thumbnail_path))

    with open(thumbnail_path, 'rb') as photo_file:
      data = photo_file.read(81000)

    self.assertEquals(getImageInfo(data), ('image/jpeg', 260, 173))
    
  def test_should_recreate_thumbnail_if_older_than_photo(self):
    photo_path = os.path.join(config.photo_dir, 'wilderness-01.jpg')
    thumbnail_path = os.path.join(config.thumbnail_dir, 'wilderness-01.jpg')
    shutil.copy2(photo_path, thumbnail_path)
    
    os.utime(thumbnail_path, (947374366, 947374366))

    thumbnail = Thumbnail('/wilderness-01.jpg')
    thumbnail_path = thumbnail.get_path()
    
    with open(thumbnail_path, 'rb') as photo_file:
      data = photo_file.read(81000)

    self.assertEquals(getImageInfo(data), ('image/jpeg', 260, 145))
    
  def test_should_handle_partial_directories(self):
    os.makedirs(os.path.join(config.thumbnail_dir, 'first', 'second'))
    
    photo_path = os.path.join(config.photo_dir, 'wilderness-01.jpg')
    thumbnail_path = os.path.join(config.thumbnail_dir, 'first', 'third', 'wilderness-01.jpg')
      
    thumbnail = Thumbnail('/wilderness-01.jpg')
    thumbnail_path = thumbnail.get_path()

  def test_should_only_resize_on_width(self):
    photo_path = os.path.join(config.photo_dir, 'boris-1.jpg')
    thumbnail_path = os.path.join(config.thumbnail_dir, 'boris-1.jpg')
    shutil.copy2(photo_path, thumbnail_path)
    
    thumbnail = Thumbnail('/boris-1.jpg')
    thumbnail_path = thumbnail.get_path()
    
    with open(thumbnail_path, 'rb') as photo_file:
      data = photo_file.read(81000)

    self.assertEquals(getImageInfo(data), ('image/jpeg', 260, 346))

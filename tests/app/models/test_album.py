import os, sys
import unittest2
import simplejson as json

from app.models.album import Album

from config import config

def delete_file(file_path):
  if os.path.exists(file_path):
    os.remove(file_path)

class TestAlbum(unittest2.TestCase):
  def setUp(self):
    self.album = Album(path='/2001/02/canoe_the_wye')
    self.album.album_dir = config.photo_dir

  def test_should_pickup_title_from_summary_yaml(self):
    self.assertEqual(self.album.title, 'Canoe the Wye')
    
  def test_should_accept_year_month_name(self):
    album = Album('2001', '02', 'canoe_the_wye')
    self.assertEqual(album.year, '2001')
    self.assertEqual(album.month, '02')
    self.assertEqual(album.name, 'canoe_the_wye')
    
    self.assertEqual(album.title, 'Canoe The Wye')
    self.assertEqual(album.url_path, '/2001/02/canoe_the_wye')
    self.assertEqual(album.album_dir, os.path.join('images', '2001', '02', 'canoe_the_wye')) 

  def test_should_accept_path(self):
    album = Album(path='/2001/02/canoe_the_wye')
    self.assertEqual(album.year, '2001')
    self.assertEqual(album.month, '02')
    self.assertEqual(album.name, 'canoe_the_wye')
    
    self.assertEqual(album.title, 'Canoe The Wye')
    self.assertEqual(album.url_path, '/2001/02/canoe_the_wye')
    self.assertEqual(album.album_dir, os.path.join('images', '2001', '02', 'canoe_the_wye')) 

  def test_list_graphic_files(self):
    expected = ['IMG_3277.jpg', 'IMG_6868.jpg',  'P9103882.jpg', 'wilderness-01.jpg', 'boris-1.jpg']
    self.assertItemsEqual(list(self.album.graphic_files()), expected)
    
  def test_first_image_url(self):
    self.assertEqual(self.album.first_image_url(), '/thumbnails/2001/02/canoe_the_wye/boris-1.jpg')

  def test_get_image_url(self):
    self.assertEqual(self.album.get_image_url('IMG_3277.jpg'), '/photos/2001/02/canoe_the_wye/IMG_3277.jpg')

  def test_get_thumbnail_url(self):
    self.assertEqual(self.album.get_thumbnail_url('IMG_3277.jpg'), '/thumbnails/2001/02/canoe_the_wye/IMG_3277.jpg')
  
  def test_read_image_data(self):
    expected = ('image/jpeg', 800, 533)
    self.assertItemsEqual(self.album.read_image_data('IMG_3277.jpg'), expected)
    
  def test_get_summary(self):
    summary = self.album.summary
    
    self.assertEqual(summary['title'], 'Canoe the Wye')
    self.assertEqual(summary['cover-image'], 'wilderness_christmas/100_0009.jpg')
    self.assertEqual(summary['summary'], 'My paragraph\n\nAnother paragraph')
    
  def test_should_read_exif_data_from_image_if_cache_file_absent(self):
    cache_path = os.path.join(config.photo_dir, config.metadata_cache_file_name)
    delete_file(cache_path)
    
    expected = {'IMG_3277.jpg': 'data', 
                'IMG_6868.jpg': 'data',
                'boris-1.jpg' : 'data',
                'wilderness-01.jpg': 'data'}
    json_expected = json.dumps(expected)
    
    expected_paths = ['2001\\02\\canoe_the_wye\\P9103882.jpg'.replace('\\', os.sep),
                      '2001\\02\\canoe_the_wye\\boris-1.jpg'.replace('\\', os.sep),
                      '2001\\02\\canoe_the_wye\\IMG_3277.jpg'.replace('\\', os.sep),
                      '2001\\02\\canoe_the_wye\\IMG_6868.jpg'.replace('\\', os.sep),
                      '2001\\02\\canoe_the_wye\\wilderness-01.jpg'.replace('\\', os.sep)]

    
    def dummy_run_exiftool(relative_paths):
      self.assertItemsEqual(relative_paths, expected_paths)
      return expected
    
    self.album.run_exiftool = dummy_run_exiftool    
    
    try:
      self.assertItemsEqual(self.album.get_exif_data(), json_expected)
      
      #should write cache file
      self.assertTrue(os.path.exists(cache_path))
      with open(cache_path, 'r') as cache_file:
        self.assertEquals(cache_file.read(), json_expected)
    finally:
      delete_file(cache_path)
    
  def test_should_read_exif_data_from_cache_file_when_present(self):
    cache_path = os.path.join(config.photo_dir, config.metadata_cache_file_name)
    delete_file(cache_path)
    
    expected = json.dumps({'dummy': 'cache_file'})
    with open(cache_path, 'w') as cache_file:
      cache_file.write(expected)
      
    try:
      self.assertEquals(self.album.get_exif_data(), expected)
    finally:
      delete_file(cache_path)
      
  def test_cache_file_can_be_deleted(self):
    cache_path = os.path.join(config.photo_dir, config.metadata_cache_file_name)
    with file(cache_path, 'a'):
      os.utime(cache_path, None)
    
    self.album.delete_metadata_cache()
    self.assertFalse(os.path.exists(cache_path))

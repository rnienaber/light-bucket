import os
import unittest2
from config import Config
from exiftool_reader import ExifToolReader

test_config = Config()
test_config.photo_dir = os.path.join(os.path.dirname(__file__), 'images')
required_image_tags = ['latitude', 'longitude', 'comment', 'keywords',
                       'title', 'date', 'make', 'model', 'subject']

reader = ExifToolReader(test_config)

class TestExifReader(unittest2.TestCase):
    def test_should_throw_an_error_if_file_doesnt_exist(self):
        err = self.assertRaises(IOError, reader.get_exif, 'NON-EXISTANT-FILE.jpg')

    def test_should_return_all_tags(self):
        tags = reader.get_exif('IMG_3277.jpg')
        self.assertItemsEqual(tags.keys(), required_image_tags)

    def test_should_return_all_tags_with_empty_tag_parameter(self):
        tags = reader.get_exif('IMG_3277.jpg', '')
        self.assertItemsEqual(tags.keys(), required_image_tags)

    def test_should_return_all_tags_with_None_tag_parameter(self):
        tags = reader.get_exif('IMG_3277.jpg', None)
        self.assertItemsEqual(tags.keys(), required_image_tags)

    def test_should_return_only_search_tags(self):
        tags = reader.get_exif('IMG_3277.jpg', 'make,model')

        self.assertEquals(len(tags.keys()), 2)
        self.assertEquals(tags['make'], 'Canon')
        self.assertEquals(tags['model'], 'Canon EOS 550D')

    def test_tag_search_should_handle_spaces_between_commas(self):
        tags = reader.get_exif('IMG_3277.jpg', '  make  ,  model  ')

        self.assertEquals(len(tags.keys()), 2)
        self.assertEquals(tags['make'], 'Canon')
        self.assertEquals(tags['model'], 'Canon EOS 550D')

    def test_tag_search_should_be_case_insensitive(self):
        tags = reader.get_exif('IMG_3277.jpg', 'Make,moDel')

        self.assertEquals(len(tags.keys()), 2)
        self.assertEquals(tags['make'], 'Canon')
        self.assertEquals(tags['model'], 'Canon EOS 550D')

    def test_should_not_return_missing_search_tags(self):
        tags = reader.get_exif('IMG_3277.jpg', 'UNKNOWN_KEY')

        self.assertEquals(len(tags.keys()), 0)

    def test_should_fix_up_GPS_coordinates(self):
        tags = reader.get_exif('IMG_3277.jpg', 'longitude,latitude')

        self.assertEquals(len(tags.keys()), 2)
        self.assertEquals(tags['latitude'], 43.493369)
        self.assertEquals(tags['longitude'], -1.554734)

    def test_should_return_comment(self):
        tags = reader.get_exif('IMG_3277.jpg', 'comment')

        self.assertEquals(len(tags.keys()), 1)
        self.assertEquals(tags['comment'], 'This is a comment')

    def test_should_return_keywords(self):
        tags = reader.get_exif('IMG_3277.jpg', 'keywords')

        self.assertEquals(len(tags.keys()), 1)
        self.assertEquals(tags['keywords'], 'keyword1,keyword2')

    def test_should_return_title(self):
        tags = reader.get_exif('IMG_3277.jpg', 'title')

        self.assertEquals(len(tags.keys()), 1)
        self.assertEquals(tags['title'], 'Title goes here')

    def test_should_return_date(self):
        tags = reader.get_exif('IMG_3277.jpg', 'date')

        self.assertEquals(len(tags.keys()), 1)
        self.assertEquals(tags['date'], '2012-06-03T18:16:49')
        
    def test_should_return_date2(self):
        tags = reader.get_exif('wilderness-01.jpg', 'date')

        self.assertEquals(len(tags.keys()), 1)
        self.assertEquals(tags['date'], '2009-01-09T08:50:41')

    def test_should_return_subject(self):
        tags = reader.get_exif('IMG_3277.jpg', 'subject')

        self.assertEquals(len(tags.keys()), 1)
        self.assertEquals(tags['subject'], 'This is a subject')

    def test_should_return_person_in_image(self):
        tags = reader.get_exif('IMG_6868.jpg', 'person_in_image')

        self.assertEquals(len(tags.keys()), 1)
        self.assertEquals(tags['person_in_image'], 'rachel,richard')

    def test_should_return_blank_if_tag_not_found(self):
        tags = reader.get_exif('IMG_3277.jpg', 'person_in_image')

        self.assertEquals(len(tags.keys()), 0)

    def test_should_return_tags_for_all_images(self):
        info = reader.get_exifs(['IMG_6868.jpg', 'IMG_3277.jpg'])

        self.assertItemsEqual(info.keys(), ['IMG_6868.jpg', 'IMG_3277.jpg'])
        self.assertTrue('person_in_image' in info['IMG_6868.jpg'])
        self.assertFalse('person_in_image' in info['IMG_3277.jpg'])

    def test_should_return_tags_for_just_one_image(self):
        info = reader.get_exifs(['IMG_6868.jpg'])

        self.assertItemsEqual(info.keys(), ['IMG_6868.jpg'])
        self.assertTrue('person_in_image' in info['IMG_6868.jpg'])

    def test_should_handle_string_value(self):
        info = reader.get_exifs('IMG_6868.jpg')

        self.assertItemsEqual(info.keys(), ['IMG_6868.jpg'])
        self.assertTrue('person_in_image' in info['IMG_6868.jpg'])
   
    def test_should_handle_locations_with_spaces(self):
        path = 'subdir with spaces/lunch_at_dave-1.jpg'
        info = reader.get_exifs(path)

        self.assertItemsEqual(info.keys(), [path])
        self.assertTrue('keywords' in info[path])

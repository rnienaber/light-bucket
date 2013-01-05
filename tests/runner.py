import sys, os
sys.path.insert(0, '../lib')
sys.path.insert(1, '../app')

import unittest2 as unittest
from config import config
config.photo_dir = os.path.join(os.path.dirname(__file__), 'images')

if __name__ == "__main__":
    loader = unittest.TestLoader()
    #all_tests = loader.loadTestsFromName('app.models.test_album.TestAlbum')

    all_tests = loader.discover('', pattern='*.py')
    unittest.TextTestRunner().run(all_tests)


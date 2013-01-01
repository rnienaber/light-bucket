import sys
sys.path.insert(0, '../lib')
sys.path.insert(1, '../app')

import unittest2 as unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    #all_tests = loader.loadTestsFromName('test_exif_reader.TestExifReader.test_should_return_date2')

    all_tests = loader.discover('', pattern='*.py')
    unittest.TextTestRunner().run(all_tests)


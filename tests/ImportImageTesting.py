# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\ImportImageTesting.py
# Derek Jennings

import unittest
import sys

sys.path.append('../image-editor')

from Classes.RequestHandler import RequestHandler

class ImportImageTesting(unittest.TestCase):
    def testing_import_with_png(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image('./sample_images/nyx.png'), True)

    def testing_import_with_jpg(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image('./sample_images/nyx_cyndaquil.jpg'), True)

    def testing_import_with_non_supported_file_type(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image('./sample_images/words.txt'), False)

    def testing_not_valid_file_path(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image( 'dpcitures'), False )


if __name__ == '__main__':
    unittest.main()
import unittest
import numpy as np
import PIL
import sys

sys.path.append('../image-editor')

from Classes.RequestHandler import RequestHandler

class ImportImageTesting(unittest.TestCase):
    def testing_import_with_png(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image('./nyx.png'), True)

    def testing_import_with_jpg(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image('./nyx_cyndaquil.jpg'), True)


    def testing_import_with_non_supported_file_type(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image('./words.txt'), False)


if __name__ == '__main__':
    unittest.main()
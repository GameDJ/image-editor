import unittest
import sys
import PIL

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
        self.assertRaises(PIL.UnidentifiedImageError, handler.import_image , './sample_images/words.txt')


    def testing_not_valid_file_path(self):
        handler = RequestHandler()
        self.assertRaises(FileNotFoundError, handler.import_image, 'dpcitures')


if __name__ == '__main__':
    unittest.main()
import unittest
import numpy as np
import PIL

from Image import Image
from ImageInitializer import ImageInitializer
from PngImporter import PngImporter
from JpegImporter import JpegImporter

class ImportImageTesting(unittest.TestCase):
    def testing_png_import_with_png(self):
        importer = PngImporter()
        image = importer.import_image('./nyx.png')
        self.assertIsNotNone(image)

    def testing_jpeg_import_with_jpg(self):
        importer = JpegImporter()
        image = importer.import_image('./nyx_cyndaquil.jpg')
        self.assertIsNotNone(image)


    #We expect the following two test cases to be not None because the code for each importer is the same
    def testing_png_import_with_jpg(self):
        importer = PngImporter()
        image = importer.import_image('./nyx_cyndaquil.jpg')
        self.assertIsNotNone(image)

    def testing_jpeg_import_with_png(self):
        importer = JpegImporter()
        image = importer.import_image('./nyx.png')
        self.assertIsNotNone(image)
        

    def testing_png_import_with_non_supported_file_type(self):
        importer = PngImporter()
        self.assertRaises(PIL.UnidentifiedImageError, importer.import_image('./words.txt'))

    def testing_jpeg_import_with_non_supported_file_type(self):
        importer = JpegImporter()
        self.assertRaises(PIL.UnidentifiedImageError, importer.import_image('./words.txt'))


if __name__ == '__main__':
    unittest.main()
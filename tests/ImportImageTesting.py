import unittest
import numpy as np

from Image import Image
from ImageInitializer import ImageInitializer
from PngImporter import PngImporter
from JpegImporter import JpegImporter


class ImportImageTesting(unittest.TestCase):
    def testing_png_import(self):
        importer = JpegImporter()
        image = importer.import_image('./nyx.png')
        self.assertIsNotNone(image)

    def testing_jpeg_import(self):
        importer = PngImporter()
        image = importer.import_image('./nyx_cyndaquil.jpg')
        self.assertIsNotNone(image)

    def testing_




if __name__ == '__main__':
    unittest.main()
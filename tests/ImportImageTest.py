# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\ImportImageTest.py

import unittest
import sys
sys.path.append("../image-editor")
from Classes.RequestHandler import RequestHandler

class ImportImageTest(unittest.TestCase):
    def test_valid_image_path(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image(""), True)
    
    def test_invalid_image_path(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image(""), False)
    
    def test_not_image(self):
        handler = RequestHandler()
        self.assertEqual(handler.import_image(""), False)
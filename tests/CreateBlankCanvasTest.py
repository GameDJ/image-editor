# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\CreateBlankCanvasTest.py

import unittest
import sys
sys.path.append("../image-editor")
from Classes import RequestHandler

class CreateBlankCanvasTest(unittest.TestCase):
    def test_valid_arguments(self):
        handler = RequestHandler()
        self.assertEqual(handler.create_canvas(10, 10, (78, 62, 128)), True)
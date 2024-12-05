# MUST BE RUN AS: python '.\Unit Testing\CreateBlankCanvasTest.py'

import unittest
import sys
sys.path.append("../image-editor")
from Classes import RequestHandler

class CreateBlankCanvasTest(unittest.TestCase):
    def test_create_blank_canvas(self):
        handler = RequestHandler()
        self.assertEqual(handler.create_canvas(10, 10, (78, 62, 128)), True)
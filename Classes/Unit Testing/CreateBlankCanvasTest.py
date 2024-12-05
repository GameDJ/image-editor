import unittest
from Classes import RequestHandler

class CreateBlankCanvasTest(unittest.TestCase):
    def test_create_blank_canvas(self):
        handler = RequestHandler()
        self.assertEqual(handler.create_canvas(10, 10, (78, 62, 128)), True)
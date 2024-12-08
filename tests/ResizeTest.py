#Will Verplaetse
# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\ResizeTest.py

import numpy as np
import unittest
import sys
sys.path.append("../image-editor")
from Classes.RequestHandler import RequestHandler

class ResizeTesting(unittest.TestCase):
  def testing_negative_size(self):
    handler = RequestHandler()
    handler.create_canvas(10, 10, (78, 62, 128))
    self.assertEqual(handler.resize((100,100)), True)

  def testing_positive_size(self):
    handler = RequestHandler()
    handler.create_canvas(10, 10, (78, 62, 128))
    self.assertEqual(handler.resize((100,100)), True)

  def testing_zero_size(self):
    handler = RequestHandler()
    handler.create_canvas(10, 10, (78, 62, 128))
    self.assertRaises(ValueError, handler.resize, (0, 0))
    

if __name__ == '__main__':
  unittest.main()
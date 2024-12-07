#Will Verplaetse
# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\CropTesting.py

import unittest
import numpy as np

import sys
sys.path.append("../image-editor")

from Classes.RequestHandler import RequestHandler


class CropTesting(unittest.TestCase):

  def testing_in_bounds(self):

    handler = RequestHandler()
    handler.create_canvas(10, 10, (78, 62, 128))
    handler.make_selection((0,0), (5,8))

    self.assertEqual(handler.crop(), True)


  def testing_out_of_bounds(self):
    handler = RequestHandler()
    handler.create_canvas(10, 10, (78, 62, 128))
    handler.make_selection((-1,-1), (1000,5000))

    self.assertEqual( handler.crop(), True)

if __name__ == "__main__":
  unittest.main()
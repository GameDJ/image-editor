#Will Verplaetse
# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\CropTesting.py

import unittest
import numpy as np

import sys
sys.path.append("../image-editor")

from Classes.image.Image import Image
from Classes.info.Arguments import Arguments
from Classes.edit.Crop import Crop
from Classes.info.Selection import Selection


class CropTesting(unittest.TestCase):

  def testing_in_bounds(self):
    orig = orig = np.full( (100,100,3), (80, 128, 40), dtype=np.uint8)
    image = Image(orig)
    the_args = Arguments(image)
    sel = Selection( (0,0), (10,5) )
    the_args.add_selection(sel)
    editor = Crop()
    edited = editor.edit(the_args)

    cropped = orig[0:10, 0:5]
    correct_im = Image(cropped)
    self.assertEqual(edited, correct_im)


  def testing_out_of_bounds(self):
    orig = orig = np.full( (100,100,3), (80, 128, 40), dtype=np.uint8)
    image = Image(orig)
    the_args = Arguments(image)
    sel = Selection( (-2,-2), (1000,500) )
    the_args.add_selection(sel)
    editor = Crop()
    edited = editor.edit(the_args)

    self.assertEqual(image, edited)

if __name__ == "__main__":
  unittest.main()
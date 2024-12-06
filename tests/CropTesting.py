#Will Verplaetse

import unittest
import numpy as np
import cv2

from Image import Image
from Arguments import Arguments
from Edit import Edit
from Crop import Crop
from Selection import Selection


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



  

    if __name__ == "__main__":
      unittest.main()
#Will Verplaetse

import numpy as np
import unittest
import cv2


from Image import Image
from Arguments import Arguments
from Edit import Edit
from SizeEditor import SizeEditor


class ResizeTesting(unittest.TestCase):
  def testing_negative_size(self):
    
    orig = np.full( (10,10,3), (80, 128, 40), dtype=np.uint8)

    image = Image(orig)
    the_args = Arguments(image)
    the_args.add_dimensions( (-100, -100))
    editor = SizeEditor()
    edited = editor.edit(the_args)
    resized = cv2.resize(orig, (100, 100))
    correct_im = Image(resized)
    self.assertEqual(edited, correct_im)


  def testing_positive_size(self):
    
    orig = np.full( (10,10,3), (80, 128, 40), dtype=np.uint8)                  
    image = Image(orig)
    the_args = Arguments(image)
    the_args.add_new_size(50, 50)
    editor = SizeEditor()
    edited = editor.edit(the_args)

    resized = cv2.resize(orig, (50, 50))
    correct_im = Image(resized)
    self.assertEqual(edited, correct_im)

  def testing_zero_size(self):
    
    orig = np.full( (10,10,3), (80, 128, 40), dtype=np.uint8)
    image = Image(orig)
    the_args = Arguments(image)
    the_args.add_dimensions((0,0))
    editor = SizeEditor()
    self.assertRaises(ValueError, editor.edit(the_args))
    




if __name__ == '__main__':
  unittest.main()
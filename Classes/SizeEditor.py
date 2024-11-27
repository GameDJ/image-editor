#This class edits the size of the image it receives as a parameter

import cv2
import numpy as np
from Edit import Edit
from Arguments import Arguments
from ArgumentType import ArgumentType as AT
from Image import Image
import numpy as np
class SizeEditor(Edit):
  @staticmethod
  def edit(args: Arguments):
    image: Image = args.get_args()[AT.IMAGE]
    image_array: np.ndarray = image.get_img_array()
    image_array = cv2.resize(image, args["new_size"])
    image.set_img_array(image_array)
    return image

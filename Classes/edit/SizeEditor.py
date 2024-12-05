#This class edits the size of the image it receives as a parameter

import cv2
import numpy as np
from Classes.edit.Edit import Edit
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
from Classes.image.Image import Image
import numpy as np
class SizeEditor(Edit):
  def edit(self, args: Arguments):
    image: Image = args.get_args()[AT.IMAGE]
    image_array: np.ndarray = image.get_img_array()
    dimensions = args.get_args()[AT.DIMENSIONS]
    image_array = cv2.resize(image_array, ( abs(dimensions[0]) , abs(dimensions[1])) )
    image.set_img_array(image_array)
    return image

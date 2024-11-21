#This Class will crop an image to within the specified dimensions

import cv2
import numpy as np
from Edit import Edit
from Arguments import Arguments
from ArgumentType import ArgumentType as AT

class Crop(Edit):
  @staticmethod
  def edit(args: Arguments):
    image = args.get_args[AT.IMAGE]
    if AT.SELECTION in args:
      bbox = args.get_args[AT.SELECTION].get_bbox()
    else:
      bbox = (0, 0, image.shape[0]-1, image.shape[1]-1)
    image = image[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    return image

import cv2
import numpy as np
import Edit

class Crop(Edit):
  def __init_(self):
    super.__init__()

  def edit(self, args, image):
    super().edit
    image = image[args["top_left_corner"][0]: args["bottom_right_corner"][0], args["top_left_corner"][1] : args["bottom_right_corner"][1]]
    return image
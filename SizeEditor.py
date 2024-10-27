import cv2
import numpy as np
import Edit
class SizeEditor(Edit):
  def __init__(self):
    super.__init__()


  def edit(self, args, image):
    image = cv2.resize(image, args["new_size"])
    return image
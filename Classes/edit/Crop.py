#This Class will crop an image to within the specified dimensions

# import cv2
# import numpy as np
from Classes.edit.Edit import Edit
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT

class Crop(Edit):
  
  def __init__(self):
    pass

  def edit(args: Arguments):
    image = args.get_args[AT.IMAGE]
    if AT.SELECTION in args:
      bbox = args.get_args[AT.SELECTION].get_bbox()
    else:
      bbox = (0, 0, image.shape[0]-1, image.shape[1]-1)
    image = image[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    return image

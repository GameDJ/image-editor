#This Class will crop an image to within the specified dimensions

# import cv2
# import numpy as np
from Classes.edit.Edit import Edit
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
from Classes.image.Image import Image

class Crop(Edit):
  def edit(self, args: Arguments) -> Image:
    image: Image = args.get_args()[AT.IMAGE]
    image_array = image.get_img_array()
    if AT.SELECTION in args.get_args():
      bbox = args.get_args()[AT.SELECTION].get_bbox()
    else:
      bbox = (0, 0, image_array.shape[0]-1, image_array.shape[1]-1)

    #Bounds checking
    if not (bbox[0] < 0 or bbox[0] > len(image_array[0]) or bbox[1] < 0 or bbox[1] > len(image_array) or bbox[2] < 0 or bbox[2] > len(image_array[0]) or bbox[3] < 0 or bbox[3] > len(image_array) ):
      image_array = image_array[bbox[1]:bbox[3], bbox[0]:bbox[2]]
      image.set_img_array(image_array)
      
    return image

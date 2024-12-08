import numpy as np
from Classes.edit.Edit import Edit
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
from Classes.info.Selection import Selection
from Classes.image.Image import Image

class DuplicateSelection(Edit):
  def edit(self, args: Arguments) -> Image:
    """This method will duplicate a selection into another area"""
    image: Image = args.get_args()[AT.IMAGE]
    image_array: np.ndarray = image.get_img_array()
    sel1: Selection = args.get_args()[AT.SELECTION]
    sel1_bbox: tuple[int, int, int, int] = sel1.get_bbox()
    sel2: Selection = args.get_args()[AT.SELECTION2]
    sel2_bbox: tuple[int, int, int, int] = sel2.get_bbox()
    
    image_array[sel2_bbox[1]:sel2_bbox[3], sel2_bbox[0]:sel2_bbox[2]] = image_array[sel1_bbox[1]:sel1_bbox[3], sel1_bbox[0]:sel1_bbox[2]]
    
    image.set_img_array(image_array)
    return image
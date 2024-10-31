import numpy as np
import Edit

class DuplicateSelection(Edit):
  def __init__(self):
    pass

  def edit(self, args, image):
    im2 = image[args['selection'].start_coordinate[0] : args['selection'].end_coordinate[0], args['selection'].start_coordinate[1] : args['selection']end_coordinate[1]]



    for row in im2:
      for col in row:
        image[args['selection2'].start_coordinate[0] + row][args['selection2'].start_coordinate[1] + col] = im2[row][col]
    
    return image
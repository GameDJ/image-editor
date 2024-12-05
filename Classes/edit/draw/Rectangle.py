from Classes.edit.draw.Shape import Shape
from Classes.image.Image import Image
from Classes.info.Selection import Selection
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
import numpy as np
# import cv2

class Rectangle(Shape):
    def apply_shape(self, image_array: np.ndarray, color: tuple[int, int, int]) -> np.ndarray:
        """Draw the shape across the given image array.  
        Arguments:
        image_array -- ONLY the part of the array to draw the shape across
        color -- RGB tuple
        """
        
        # apply rectangle
        # image_array = color
        
        return np.full(image_array.shape, color)
import Edit
import Arguments
import Image
from enum import Enum, auto
import numpy as np
import cv2
import FilterType

class Filters(Edit):
    def __init__(self, image: Image):
        self.image = image

    def edit(self, filter_type: FilterType, args: Arguments, image: Image)->Image:
        if filter_type == FilterType.BLUR:
            self.image = self.blur(self.image, args.get_args()["amount"])
        elif filter_type == FilterType.INVERT:
            self.image = self.invert(self.image)
        elif filter_type == FilterType.FLIP_HORIZONTAL:
            self.image = self.flipHorizontal(self.image)
        elif filter_type == FilterType.FLIP_VERTICAL:
            self.image = self.flipVertical(self.image)
        elif filter_type == FilterType.GRAYSCALE:
            self.image = self.grayscale(self.image)
        elif filter_type == FilterType.ADJUST_BRIGHTNESS:
            self.image = self.adjustBrightness(self.image, args.get_args()["amount"])

    def blur(self, image: Image, kernel_size: int)->Image:
        return cv2.GaussianBlur(self.image, (kernel_size, kernel_size), 0)
    
    def invert(self, image: Image)->Image:
        return 255-self.image
    
    def flipHorizontal(self, image: Image)->Image:
        return np.flip(image, axis = 1)

    def flipVertical(self, image: Image)->Image:
        return np.flip(image, axis = 0)

    def grayscale(self, image: Image)->Image:
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    def adjustBrightness(self, image: Image, amount: float)->Image:
        return  np.clip(self.image * amount, 0, 255).astype(np.uint8)
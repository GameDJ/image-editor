from Edit import Edit
from Arguments import Arguments
from ArgumentType import ArgumentType as AT
from Image import Image
from enum import Enum, auto
import numpy as np
import cv2
from FilterType import FilterType

class Filters(Edit):
    @staticmethod
    def edit(args: Arguments)->Image:
        filter_type = args.get_args()[AT.FILTER]
        image = args.get_args()[AT.IMAGE]
        if filter_type == FilterType.BLUR:
            image = Filters._blur(image, args.get_args()[AT.AMOUNT])
        elif filter_type == FilterType.INVERT:
            image = Filters._invert(image)
        elif filter_type == FilterType.FLIP_HORIZONTAL:
            image = Filters._flipHorizontal(image)
        elif filter_type == FilterType.FLIP_VERTICAL:
            image = Filters._flipVertical(image)
        elif filter_type == FilterType.GRAYSCALE:
            image = Filters._grayscale(image)
        elif filter_type == FilterType.ADJUST_BRIGHTNESS:
            image = Filters._adjustBrightness(image, args.get_args()[AT.AMOUNT])
        return image

    @staticmethod
    def _blur(image: Image, kernel_size: int)->Image:
        def nearest_odd_int(num: float) -> int:
            num = int(num)
            if num % 2 == 0:
                num += 1
            return num
        # convert RGB numpy array to BGR cv2 array
        cv2_mat = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # perform blur operation
        kernel_size = nearest_odd_int(kernel_size)
        blurred = cv2.GaussianBlur(cv2_mat, (int(kernel_size), int(kernel_size)), 0)
        # convert BGR cv2 array back to RGB numpy array and return
        m, n, c = blurred.shape
        rgb_blurred = blurred[0:m:1, 0:n:1, -1::-1]
        return np.array(rgb_blurred)
    
    @staticmethod
    def _invert(image: Image)->Image:
        return 255 - image
    
    @staticmethod
    def _flipHorizontal(image: Image)->Image:
        return np.flip(image, axis = 1)

    @staticmethod
    def _flipVertical(image: Image)->Image:
        return np.flip(image, axis = 0)

    @staticmethod
    def _grayscale(image: Image)->Image:
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    @staticmethod
    def _adjustBrightness(image: Image, amount: float)->Image:
        return np.clip(image * amount, 0, 255).astype(np.uint8)
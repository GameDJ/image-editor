from Classes.Edit import Edit
from Classes.Arguments import Arguments
from Classes.ArgumentType import ArgumentType as AT
from Classes.Image import Image
from Classes.Selection import Selection
from enum import Enum, auto
import numpy as np
import cv2
from Classes.FilterType import FilterType

class Filters(Edit):
    @staticmethod
    def edit(args: Arguments) -> Image:
        full_image: Image = args.get_args()[AT.IMAGE]
        full_image_array: np.ndarray = full_image.get_img_array()
        filter_type: FilterType = args.get_args()[AT.FILTER]
        
        # If selection is active, we're just going to edit that part of the image
        if AT.SELECTION in args.get_args():
            using_selection = True
            sel: Selection = args.get_args()[AT.SELECTION]
            sel_bbox: tuple[int, int, int, int] = sel.get_bbox()
            image_edit_area = full_image_array[sel_bbox[1]:sel_bbox[3], sel_bbox[0]:sel_bbox[2]]
        else:
            using_selection = False
            image_edit_area = full_image_array
            
        # Perform the edit
        if filter_type == FilterType.BLUR:
            image_edit_area = Filters._blur(image_edit_area, args.get_args()[AT.AMOUNT])
        elif filter_type == FilterType.INVERT:
            image_edit_area = Filters._invert(image_edit_area)
        elif filter_type == FilterType.FLIP_HORIZONTAL:
            image_edit_area = Filters._flipHorizontal(image_edit_area)
        elif filter_type == FilterType.FLIP_VERTICAL:
            image_edit_area = Filters._flipVertical(image_edit_area)
        elif filter_type == FilterType.GRAYSCALE:
            image_edit_area = Filters._grayscale(image_edit_area)
        elif filter_type == FilterType.ADJUST_BRIGHTNESS:
            image_edit_area = Filters._adjustBrightness(image_edit_area, args.get_args()[AT.AMOUNT])
        
        # Apply the edited selection area to the full image array (if applicable) 
        if using_selection:
            full_image_array[sel_bbox[1]:sel_bbox[3], sel_bbox[0]:sel_bbox[2]] = image_edit_area
        else:
            full_image_array = image_edit_area
        
        full_image.set_img_array(full_image_array)
        return full_image

    @staticmethod
    def _blur(image: np.ndarray, kernel_size: int)->np.ndarray:
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
    def _invert(image: np.ndarray)->np.ndarray:
        return 255 - image
    
    @staticmethod
    def _flipHorizontal(image: np.ndarray)->np.ndarray:
        return np.flip(image, axis = 1)

    @staticmethod
    def _flipVertical(image: np.ndarray)->np.ndarray:
        return np.flip(image, axis = 0)

    @staticmethod
    def _grayscale(image: np.ndarray)->np.ndarray:
        # calculate Luminance value of each RGB cell
        grayed_L: np.ndarray = np.dot(image, [0.299, 0.587, 0.114])
        # round each value back to an int
        grayed_L = np.ndarray.round(grayed_L).astype(np.uint8)
        # convert the single Luminance value back to a triple RGB value
        grayed_RGB = np.stack([grayed_L] * 3, axis=2)
        return grayed_RGB
    
    @staticmethod
    def _adjustBrightness(image: np.ndarray, amount: float)->np.ndarray:
        return np.clip(image * amount, 0, 255).astype(np.uint8)
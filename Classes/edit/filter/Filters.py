from Classes.edit.Edit import Edit
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
from Classes.image.Image import Image
from Classes.info.Selection import Selection
from enum import Enum, auto
import numpy as np
import cv2
from Classes.edit.filter.FilterType import FilterType

class Filters(Edit):
    def edit(self, args: Arguments) -> Image:
        """Applys a filter either to the entire image or to the given selection.
        Arguments:
        image -- Image to edit
        selection -- (optional) selection area in which to apply the filter
        amount -- (optional) used for blur and bridghtness
        
        Returns:
        The edited image.
        """
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
            image_edit_area = self._blur(image_edit_area, args.get_args()[AT.AMOUNT])
        elif filter_type == FilterType.INVERT:
            image_edit_area = self._invert(image_edit_area)
        elif filter_type == FilterType.FLIP_HORIZONTAL:
            image_edit_area = self._flipHorizontal(image_edit_area)
        elif filter_type == FilterType.FLIP_VERTICAL:
            image_edit_area = self._flipVertical(image_edit_area)
        elif filter_type == FilterType.GRAYSCALE:
            image_edit_area = self._grayscale(image_edit_area)
        elif filter_type == FilterType.ADJUST_BRIGHTNESS:
            image_edit_area = self._adjustBrightness(image_edit_area, args.get_args()[AT.AMOUNT])
        
        # Apply the edited selection area to the full image array (if applicable) 
        if using_selection:
            full_image_array[sel_bbox[1]:sel_bbox[3], sel_bbox[0]:sel_bbox[2]] = image_edit_area
        else:
            full_image_array = image_edit_area
        
        full_image.set_img_array(full_image_array)
        return full_image

    def _blur(self, image: np.ndarray, kernel_size: int)->np.ndarray:
        if kernel_size < 0:
            raise ValueError
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
    
    def _invert(self, image: np.ndarray)->np.ndarray:
        return 255 - image
    
    def _flipHorizontal(self, image: np.ndarray)->np.ndarray:
        return np.flip(image, axis = 1)

    def _flipVertical(self, image: np.ndarray)->np.ndarray:
        return np.flip(image, axis = 0)

    def _grayscale(self, image: np.ndarray)->np.ndarray:
        # calculate Luminance value of each RGB cell
        grayed_L: np.ndarray = np.dot(image, [0.299, 0.587, 0.114])
        # round each value back to an int
        grayed_L = np.ndarray.round(grayed_L).astype(np.uint8)
        # convert the single Luminance value back to a triple RGB value
        grayed_RGB = np.stack([grayed_L] * 3, axis=2)
        return grayed_RGB
    
    def _adjustBrightness(self, image: np.ndarray, amount: float)->np.ndarray:
        return np.clip(image * amount, 0, 255).astype(np.uint8)
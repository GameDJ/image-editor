from Classes.image.Image import Image
from Classes.info.Arguments import Arguments
import numpy as np

class Shape:    
    def apply_shape(self, image_array: np.ndarray, args: Arguments) -> Image:
        raise NotImplementedError
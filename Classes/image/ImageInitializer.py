from Classes.image.Image import Image
import numpy as np

class ImageInitializer:
    """Class to initialize an Image"""
    
    def __init__(self) -> None:
        pass
    
    def import_image(self, path: str) -> Image:
        pass
    
    def create_blank_canvas(self, width: int, height: int, color: tuple[int, int, int]) -> Image:
        if width == 0 or height == 0:
            raise ValueError # i currently don't know where this will be caught at
        return Image(np.full((abs(height), abs(width), 3), color, dtype=np.uint8))
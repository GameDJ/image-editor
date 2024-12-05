from Classes.image.Image import Image
import numpy as np

class ImageInitializer:
    """Class to initialize an Image"""
    
    def __init__(self) -> None:
        pass
    
    def import_image(self, path: str) -> Image:
        pass
    
    def create_blank_canvas(self, width: int, height: int, color: tuple[int, int, int]) -> Image:
        return Image(np.full((height, width, 3), color, dtype=np.uint8))
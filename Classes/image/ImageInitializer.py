from Classes.image.Image import Image
from Classes.edit.draw.Color import Color

class ImageInitializer:
    """Class to initialize an Image"""
    
    def __init__(self) -> None:
        pass
    
    def import_image(self, path: str) -> Image:
        pass
    
    def create_blank_canvas(self, width: int, height: int, color: Color) -> Image:
        # this needs to create a numpy array with specified size (width, height) and backgroud color (color) but idk how to do that
        pass
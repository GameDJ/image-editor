from Classes.image.ImageInitializer import ImageInitializer
from Classes.image.Image import Image
from PIL import Image as PilImage
import numpy as np

class PngImporter(ImageInitializer):
    """Class to import an Image of type .png"""
    
    def __init__(self) -> None:
        super().__init__()
    
    def import_image(self, path: str) -> Image:
        image = PilImage.open(path).convert('RGB')
        if not image:
            return None
        return Image(np.array(image))
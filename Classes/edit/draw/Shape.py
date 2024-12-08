from Classes.image.Image import Image
from Classes.info.Arguments import Arguments

class Shape:    
    def apply_shape(self, image: Image, color: tuple[int, int, int]) -> Image:
        raise NotImplementedError
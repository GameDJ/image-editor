from Classes.image.Image import Image
from Classes.info.Arguments import Arguments

class Shape:    
    def apply_shape(self, image: Image, args: Arguments) -> Image:
        raise NotImplementedError
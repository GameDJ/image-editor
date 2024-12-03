from Classes.image.Image import Image

class ImageRenderer:
    """Class for holding an image intended for rendering.  
    This uses the decorator pattern, where there will be one concrete subclass
    (BasicImageRenderer) which is just for the plain image, and one abstract subclass
    (RenderAddon) which will be extended by decorator addons."""
    def __init__(self, image: Image) -> None:
        """Initialize with a copy of the given image"""
        self.image = image.__deepcopy__()
        
    def render_image(self) -> Image:
        pass
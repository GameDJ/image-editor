from Classes.Image import Image
from Classes.ImageRenderer import ImageRenderer

class BasicImageRenderer(ImageRenderer):
    """Stores a basic Image, ready for rendering."""
    def __init__(self, image: Image) -> None:
        """Initialize with a copy of the given image"""
        super().__init__(image)
        
    def render_image(self) -> Image:
        return self.image
from Classes.image.render.ImageRenderer import ImageRenderer
from Classes.image.Image import Image

class RenderAddon(ImageRenderer):
    """Parent class for decorator addons."""
    def __init__(self, renderer: ImageRenderer):
        """Store a renderer which has already been initialized"""
        self.renderer = renderer
        
    def render_image(self) -> Image:
        """Return the image stored in the renderer"""
        self.renderer.render_image()
        
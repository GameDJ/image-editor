from Classes.info.Selection import Selection
from Classes.edit.draw.Shape import Shape
from Classes.image.render.ImageRenderer import ImageRenderer
from Classes.image.render.RenderAddon import RenderAddon
from Classes.image.Image import Image
from Classes.info.Arguments import Arguments
from Classes.edit.draw.DrawShape import DrawShape

class ShapeRenderer(RenderAddon):
    def __init__(self, renderer: ImageRenderer, args: Arguments):
        """Store the renderer and draw onto its image"""
        super().__init__(renderer)
        # get the image from any previous render operations and add it to args
        args.add_image(self.renderer.render_image())
        self.draw_shape(args)
      
    def render_image(self) -> Image:
        return self.renderer.render_image()
        
    def draw_shape(self, args: Arguments) -> None:
        """Draw the shape onto the image's array"""
        DrawShape.edit(args)
        
        
        
        
        
        
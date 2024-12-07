from Classes.image.render.ImageRenderer import ImageRenderer
from Classes.image.render.RenderAddon import RenderAddon
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
from Classes.image.Image import Image
import cv2

class ZoomRenderer(RenderAddon):
    """Adds a selection box onto the image of an existing ImageRenderer."""
    def __init__(self, renderer: ImageRenderer, args: Arguments):
        """Store the renderer and draw onto its image.
        
        args should include Amount (the zoom factor) and Dimensions (the max bounds)
        """
        super().__init__(renderer)
        self.zoom(args)
      
    def render_image(self) -> Image:
        return self.renderer.render_image()
        
    def zoom(self, args: Arguments) -> None:
        """Draw a selection box onto an Image"""
        image_array = self.renderer.render_image().get_img_array()
        factor = int(args.get_args()[AT.AMOUNT])
        # validate factor
        if factor == 0:
            return
        elif factor < 0:
            # for negative factors, convert to fraction
            # (-1 becomes 1/2, -2 becomes 1/3)
            factor = 1 / abs((factor - 1))
        dimensions: tuple[int, int] = args.get_args()[AT.DIMENSIONS]
        # validate dimensions
        if min(dimensions) <= 0:
            return

        height, width = image_array.shape[0:2]
        if factor >= 1: # zoom in from base
            # we're gonna pretend the dimensions are smol, so that we can
            # crop the image first and thus have less data to resize.
            # though, these pretend-dimensions will result in a slightly larger
            # image than the viewport, to ensure we can crop it down a bit more
            # and have an exact result.
            reversefactor_dimensions = (int(dimensions[0]//factor+1), int(dimensions[1]//factor+1))
            # print(reversefactor_dimensions, "rev")
            # determine how much on each axis will overflow past the view bounds
            width_overflow = width - reversefactor_dimensions[0]
            if width_overflow < 0:
                width_overflow = 0
            height_overflow = height - reversefactor_dimensions[1]
            if height_overflow < 0:
                height_overflow = 0
            # print(width_overflow, height_overflow, "overflows")
            # determine the bounds
            left = width_overflow//2
            right = width - width_overflow//2
            top = height_overflow//2
            bot = height - height_overflow//2
            # print(left, right, "\n", top, bot, "bounds")
            # crop the pre-resized image
            image_array = image_array[top:bot, left:right]
            # print(image_array.shape, "shape after first crop")
            
            new_width = factor * (right - left)
            new_height = factor * (bot - top)
            # print(new_width, new_height, "news")
            
            # resize
            image_array = cv2.resize(image_array, (new_width, new_height))
            # print(image_array.shape, "shape after resize")
            # crop the resized image to exact dimensions
            image_array = image_array[:dimensions[1], :dimensions[0]]
            # print(image_array.shape, "shape after final crop")
        else:
            # zoom out from base
            new_width = int(factor * width)
            new_height = int(factor * height)
            image_array = cv2.resize(image_array, (new_width, new_height))
        
        self.renderer.render_image().set_img_array(image_array)
        
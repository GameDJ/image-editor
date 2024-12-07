from Classes.info.Selection import Selection
from Classes.image.render.ImageRenderer import ImageRenderer
from Classes.image.render.RenderAddon import RenderAddon
from Classes.image.Image import Image

class SelectionRenderer(RenderAddon):
    """Adds a selection box onto the image of an existing ImageRenderer."""
    def __init__(self, renderer: ImageRenderer, selection: Selection):
        """Store the renderer and draw onto its image"""
        super().__init__(renderer)
        self.draw_selection_box(selection)
      
    def render_image(self) -> Image:
        return self.renderer.render_image()
        
    def draw_selection_box(self, selection: Selection) -> bool:
        """Draw a selection box onto an Image"""
        image_array = self.renderer.render_image().get_img_array()
        LEFT, TOP, RIGHT, BOT = selection.get_bbox()
        IMG_BOTRIGHT = (image_array.shape[0]-1, image_array.shape[1]-1)
        
        # outline selection area with inverted pixels
        for i in range(LEFT, RIGHT):
            # upper bound
            if LEFT > 0 and TOP > 0:
                if (i - LEFT) % 8 < 4:
                    image_array[TOP, i] = 255 - image_array[TOP, i]
            # lower bound
            if RIGHT < IMG_BOTRIGHT[0] and BOT < IMG_BOTRIGHT[1]-1:
                if (i - LEFT) % 8 < 4:
                    image_array[BOT, i] = 255 - image_array[BOT, i]
        for i in range(TOP+1, BOT+1):
            # left bound
            if TOP > 0 and LEFT > 0:
                if (i - TOP+1) % 8 < 4:
                    image_array[i, LEFT] = 255 - image_array[i, LEFT]
            # right bound
            if BOT < IMG_BOTRIGHT[1] and RIGHT < IMG_BOTRIGHT[0]-1:
                if (i - TOP+1) % 8 < 4:
                    image_array[i, RIGHT] = 255 - image_array[i, RIGHT]
                    
        self.renderer.render_image().set_img_array(image_array)
        return True
        
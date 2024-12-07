from Classes.image.file.ImageExporter import ImageExporter
from Classes.image.Image import Image
from PIL import Image as PilImage

class PngExporter(ImageExporter):
    """Class to export an Image of type .png to the user's local storage"""
    
    def __init__(self) -> None:
        super().__init__()
        
    def export_image(self, image: Image, path: str) -> bool:
        save_image = PilImage.fromarray(image.get_img_array())
        if save_image.mode != "RGB":
            save_image = save_image.convert("RGB")
        save_image.save(path)
        return True
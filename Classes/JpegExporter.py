import ImageExporter
import Image
from PIL import Image as PilImage

class JpegExporter(ImageExporter):
    """Class to export an Image of type .jpeg to the user's local storage"""
    
    def __init__(self) -> None:
        super.__init__()
        
    def export_image(image: Image, path: str) -> None:
        save_image = PilImage.fromarray(image.get_img_array())
        save_image.save(path)
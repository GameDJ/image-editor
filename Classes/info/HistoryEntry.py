from numpy import ndarray
from Classes.image.Image import Image

class HistoryEntry:
    """Class to hold an entry for the history."""
    
    def __init__(self, image: Image, change_desc: str):
        self.image = image
        self.change_desc = change_desc
        
    def get_image(self) -> ndarray:
        return self.image
    
    def get_description(self) -> str:
        return self.change_desc
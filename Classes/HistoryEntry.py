from numpy import ndarray

class HistoryEntry:
    """Class to hold an entry for the history."""
    
    def __init__(self, image_array: ndarray, change_desc: str):
        self.image_array = image_array
        self.change_desc = change_desc
        
    def get_image(self) -> ndarray:
        return self.image_array
    
    def get_description(self) -> str:
        return self.change_desc
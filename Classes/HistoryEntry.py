import numpy as np

class HistoryEntry:
    def __init__(self, image_array: np.ndarray, change_desc: str):
        self.image_array = image_array
        self.change_desc = change_desc
        
    def get_image(self):
        return self.image_array
    
    def get_description(self):
        return self.change_desc
import numpy as np
import HistoryEntry as Entry

class History:
    def __init__(self):
        self.array_history = []
        self.index = -1

    def add_record(self, image_array: np.ndarray, change_desc: str):
        if (len(self.array_history) > self.index+1):
            # we are in the "past", so chop off any "future" entries
            self.array_history = self.array_history[0:self.index]
        new_entry = Entry(image_array, change_desc)
        self.array_history.append(new_entry)
        self.index += 1
        
    # can also trigger the above function using +=
    def __iadd__(self, image_array: np.ndarray, change_desc: str):
        self.add_record(image_array, change_desc)
    
    def get_current_img(self) -> np.ndarray:
        return self.array_history[self.index].get_image()
    
    def undo(self):
        if (self.index > 0):
            self.index -= 1
    
    def redo(self):
        if (self.index < len(self.array_history-1)):
            self.index += 1
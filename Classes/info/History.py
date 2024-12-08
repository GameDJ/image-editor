from Classes.info.HistoryEntry import HistoryEntry as Entry
from Classes.image.Image import Image

class History:
    """Class to keep track of the edit history of an Image."""
    
    def __init__(self):
        self.array_history: list[Entry] = []
        # index of the current list (does not include deleted entries)
        self.index = -1 
        # total index of the current oldest value in the list (includes deleted)
        self.oldest_index = 0
        self.MAX_LENGTH = 10

    def add_record(self, image: Image, change_desc: str) -> bool:
        """Adds an entry to the history."""
        history_len = len(self.array_history)
        if history_len > self.index+1:
            # we are in the "past", so chop off any "future" entries
            self.array_history = self.array_history[0:self.index+1]
        new_entry = Entry(image, change_desc)
        if history_len == self.MAX_LENGTH:
            # reached max entries; delete the oldest
            del self.array_history[0]
            self.oldest_index += 1
            # offset the index so it ends up staying in place
            self.index -= 1
        self.array_history.append(new_entry)
        if history_len == 1:
            # first entry
            self.oldest_index = 0
        self.index += 1
        return True
        
    # can also trigger the above function using +=
    def __iadd__(self, image: Image, change_desc: str):
        self.add_record(image, change_desc)
    
    def get_current_img(self) -> Image:
        """Returns a deep copy of the current entry's Image"""
        if self.index > -1:
            return self.array_history[self.index].get_image().__deepcopy__()
        else:
            return None
        
    def is_active_image(self) -> bool:
        """Checks if there is an active image"""
        return (self.index > -1)
    
    
    def undo(self) -> bool:
        """Undoes the recent history entry."""
        if (self.index > 0):
            self.index -= 1
            return True
        return False
    
    def redo(self) -> bool:
        """Redoes the recent history entry."""
        if (self.index < len(self.array_history)-1):
            self.index += 1
            return True
        return False
            
    def get_entry_descriptions(self) -> list[tuple[int, str]]:
        """Returns list of entry descriptions in the format [(index, description), ...]"""
        entries = []
        for i in range(len(self.array_history)):
            entries.append((i, f"{i+self.oldest_index+1}: {self.array_history[i].change_desc}"))
        return entries
  
    def set_index(self, new_index: int) -> bool:
        """Sets the current index of the history"""  
        if new_index < 0 or new_index >= self.get_length():
            return False
        self.index = new_index
        return True
    
    def get_index(self) -> int:
        return self.index
    
    def get_length(self) -> int:
        return len(self.array_history)
class Selection:
    """Class to hold the coordinates of the current selection from an Image."""
    
    def __init__(self, start_coord: int, end_coord: int):
        self.start_coordinate = start_coord
        self.end_coordinate = end_coord
        
    def get_start_coord(self) -> int:
        return self.start_coordinate
    
    def get_end_coord(self) -> int:
        return self.end_coordinate
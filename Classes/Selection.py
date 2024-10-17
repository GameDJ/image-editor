class Selection:
    def __init__(self, start_coord, end_coord):
        self.start_coordinate = start_coord
        self.end_coordinate = end_coord
        
    def get_start_coord(self):
        return self.start_coordinate
    
    def get_end_coord(self):
        return self.end_coordinate
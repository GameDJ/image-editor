import numpy as np

class Selection:
    """Class to hold the coordinates of the current selection from an Image."""
    
    def __init__(self, start_coord: tuple[int, int], end_coord: tuple[int, int]):
        self.bbox = self._calc_bbox(start_coord, end_coord)
        
    def _calc_bbox(self, start_coord: tuple[int, int], end_coord: tuple[int, int]) -> tuple[int, int, int, int]:
        """Takes two coordinates and returns a tuple representing the bounds
        Returns:
        (x_min, y_min, x_max, y_max)
        """
        x_min = min(start_coord[0], end_coord[0])
        y_min = min(start_coord[1], end_coord[1])
        x_max = max(start_coord[0], end_coord[0])
        y_max = max(start_coord[1], end_coord[1])
        return (x_min, y_min, x_max, y_max)
        
        
    # def get_start_coord(self) -> int:
    #     return self.start_coordinate
    
    # def get_end_coord(self) -> int:
    #     return self.end_coordinate
    
    def get_bbox(self) -> tuple[int, int, int, int]:
        return self.bbox
    
    def draw_selection(self, image_array: np.ndarray) -> np.ndarray:
        """Draw a selection box onto an RGB numpy array"""
        LEFT, TOP, RIGHT, BOT = self.bbox
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
        return image_array

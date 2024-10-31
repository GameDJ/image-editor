from numpy import ndarray

class Image:
    def __init__(self, img_array: ndarray) -> None:
        self.img_array = img_array
        
    def get_img_array(self) -> ndarray:
        return self.img_array
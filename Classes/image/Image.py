from numpy import ndarray

class Image:
    def __init__(self, img_array: ndarray) -> None:
        self.img_array = img_array
        
    def get_img_array(self) -> ndarray:
        return self.img_array
    
    def set_img_array(self, new_img_array: ndarray):
        self.img_array = new_img_array
        
    def __deepcopy__(self):
        return type(self)(self.img_array.copy())
        
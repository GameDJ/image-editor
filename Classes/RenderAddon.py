import numpy as np

class NdarrayAddon(np.ndarray):
    def __new__(cls, input_array, *args, **kwargs):
        obj = np.asarray(input_array).view(cls)
        return obj
    
    def __init__(self, input_array, *args, **kwargs):
        pass
        
    def copify(self) -> np.ndarray:
        return self.copy()
        
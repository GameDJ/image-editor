from RenderAddon import NdarrayAddon
import numpy as np
from Selection import Selection

class SelectionRenderer(NdarrayAddon):
    # def __init__(self, ndarray: np.ndarray):
    #     self.super(ndarray)
      
    def add_selection(self, sel: Selection):
        self.selection = sel
        
    def copify(self) -> np.ndarray:
        output = self.copy()
        if self.selection:
            output *= self.selection
        return output

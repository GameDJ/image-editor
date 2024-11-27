from Classes.SelectionRenderer import SelectionRenderer
from RenderAddon import NdarrayAddon
import numpy as np

if __name__ == "__main__":
    my_arr = np.full((2,2), 5)
    print(my_arr)
    ren = SelectionRenderer(my_arr)
    ren.add_selection(3)
    print(ren.copify())
    print(ren.shape)

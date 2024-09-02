
import sys
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

# Load an image
def load_image(path: str) -> np.ndarray:
    # image = Image.open(path).convert('L')  # Convert to grayscale
    image = Image.open(path).convert('RGB')  # Convert to RGB
    return np.array(image)

# Save a 2D array as an image
def save_image(array: np.ndarray, path: str):
    image = Image.fromarray(array)
    image.save(path)

############## History operations #################

class History:
    def __init__(self):
        self.array_history = []
        self.index = -1

    def add_record(self, image_array: np.ndarray):
        if (len(self.array_history) > self.index+1):
            # we are in the "past", so chop off any "future" entries
            self.array_history = self.array_history[0:self.index]
        self.array_history.append(image_array)
        self.index += 1
    # can also trigger the above function using +=
    def __iadd__(self, image_array: np.ndarray):
        self.add_record(image_array)
    
    def get_current_img(self) -> np.ndarray:
        return self.array_history[self.index]
    
    def undo(self):
        if (self.index > 0):
            self.index -= 1
    
    def redo(self):
        if (self.index < len(self.array_history-1)):
            self.index += 1

#################################################
############## Image operations #################

# Invert an image (RGB)
def invert_image(image_array: np.ndarray) -> np.ndarray:
    return 255 - image_array

def plus_amount(image_array: np.ndarray, amount: int) -> np.ndarray:
    return image_array + amount

def flip_horizontal(image_array: np.ndarray) -> np.ndarray:
    return np.flip(image_array, axis = 1) # flip horizontal (flip columns)

def flip_vertical(image_array: np.ndarray) -> np.ndarray:
    return np.flip(image_array, axis = 0) # flip vertical (flip rows)

# add your function here, then add a corresponding button below!

# def func_name_here(image_array: np.ndarray) -> np.ndarray:
    # return image_array
    
# def func_name_here(image_array: np.ndarray) -> np.ndarray:
    # return image_array
    
# def func_name_here(image_array: np.ndarray) -> np.ndarray:
    # return image_array
    
# def func_name_here(image_array: np.ndarray) -> np.ndarray:
    # return image_array


############## GUI operations #################

# add a button for your function here!
img_operation_buttons = (
#   (button text, function reference, args...)
    ("Invert", invert_image),
    ("Add 64", plus_amount, 64),
    ("Flip horizontal", flip_horizontal),
    ("Flip vertical", flip_vertical),
)
    
def close_window(window: tk.Tk):
    window.destroy()
        
# Generate the GUI window
# def gui(image_array: np.ndarray):
def gui(history: History):
    # convert array to PIL Image
    image = Image.fromarray(history.get_current_img())
    # initialize toplevel tkinter widget
    window = tk.Tk()
    window.title("Image Processor")

    # use ImageTk library to convert PIL image to Tk image
    tk_image = ImageTk.PhotoImage(image)

    # create a label to hold the image
    img_preview = tk.Label(window, image=tk_image)
    # give the widget to the packer (geometry manager)
    img_preview.pack()
    
    def update_img_preview(label: tk.Label):
        new_image = Image.fromarray(history.get_current_img())
        new_tk_image = ImageTk.PhotoImage(new_image)
        # update the image label
        label.config(image=new_tk_image)
        # prevent garbage collector from deleting image?
        label.image = new_tk_image
        
    def img_operation(func, *args):
        # perform the operation and add it to the history
        history.add_record(func(history.get_current_img(), *args))
        update_img_preview(img_preview)

    for buttonData in img_operation_buttons:
        if len(buttonData) <= 2:
            # function is a lambda so it can take arguments
            # "func=" thing is to save the current value within the loop; otherwise it would check buttonData[1] upon execution
            button = tk.Button(text=buttonData[0], command=lambda func=buttonData[1]: img_operation(func))
        else:
            button = tk.Button(text=buttonData[0], command=lambda func=buttonData[1], args=buttonData[2]: img_operation(func, args))
        button.pack()
    
    button = tk.Button(text="Close window", command=lambda: close_window(window))
    button.pack()

    # render the window
    window.mainloop()
    
#################################################

if __name__ == "__main__":
    # set up history
    history = History()
    
    # Load the image
    history.add_record(load_image(sys.argv[1]))
    
    # display the window
    gui(history)
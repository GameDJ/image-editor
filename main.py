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
    
def normalize_coord_pair(coord_1: tuple[int, int], coord_2: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    """takes a pair of coordinates (such as which define a rectangle), and returns the 
    coordinates of the rectangle's top left and bottom right corners, in that order"""
    x_coords = [coord_1[0], coord_2[0]]
    y_coords = [coord_1[1], coord_2[1]]
    x_coords.sort()
    y_coords.sort()
    return ((x_coords[0], y_coords[0]), (x_coords[1], y_coords[1]))

# TODO: optional: make the marching ants march &calculate the perimeter as a continuous line
def apply_marching_ants_border(image_array: np.ndarray, selection: list[tuple[int, int], tuple[int, int]], max_botright: tuple[int, int]):
    normalized = normalize_coord_pair(selection[0], selection[1])
    
    LEFT = normalized[0][0]-1
    TOP = normalized[0][1]-1
    RIGHT = normalized[1][0]
    BOT = normalized[1][1]
    
    # outline selection with inverted pixels
    for i in range(LEFT, RIGHT):
        # upper bound
        if LEFT > 0 and TOP > 0:
            if (i - LEFT) % 8 < 4:
                image_array[TOP, i] = 255 - image_array[TOP, i]
        # lower bound
        if RIGHT < max_botright[0] and BOT < max_botright[1]-1:
            if (i - LEFT) % 8 < 4:
                image_array[BOT, i] = 255 - image_array[BOT, i]
    for i in range(TOP+1, BOT+1):
        # left bound
        if TOP > 0 and LEFT > 0:
            if (i - TOP+1) % 8 < 4:
                image_array[i, LEFT] = 255 - image_array[i, LEFT]
        # right bound
        if BOT < max_botright[1] and RIGHT < max_botright[0]-1:
            if (i - TOP+1) % 8 < 4:
                image_array[i, RIGHT] = 255 - image_array[i, RIGHT]
    return image_array
        
# Generate the GUI window
def gui(history: History):
    # TODO: smallify large images
    # convert array to PIL Image
    image = Image.fromarray(history.get_current_img())
    # initialize toplevel tkinter widget
    window = tk.Tk()
    window.title("SIMPLE - Simple IMage Processor for Lazy Editors")

    # use ImageTk library to convert PIL image to Tk image
    tk_image = ImageTk.PhotoImage(image)

    # create a label to hold the image
    img_preview = tk.Label(window, image=tk_image, borderwidth=0, cursor="circle")
    # give the widget to the packer (geometry manager)

    # testing mouse-press, mouse-release, and click-and-drag #
    # https://tkinterexamples.com/events/mouse/

    # def clicked(event):
    #     print("clicked at", event.x, event.y)
    # img_preview.bind("<ButtonPress-1>", clicked)
    
    # def released(event):
    #     print("\nreleased at", event.x, event.y)
    # img_preview.bind("<ButtonRelease-1>", released)
    
    # def drag_handler(event):
    #     print(f"({event.x}, {event.y})")
    # img_preview.bind("<B1-Motion>", drag_handler)
    ##########################################################
    
    img_preview.pack()      
      
    # define variables for selection area
    # ((top-left inclusive), (bottom-right exclusive))
    # NOTE that X,Y coordinate system is opposite of row,col array system!!! 
    selection = [
        (0,0), 
        (len(history.get_current_img()[0]), len(history.get_current_img()))
    ]
    using_selection = False
    
    def reset_selection():
        selection[0] = (0,0),
        selection[1] = (len(history.get_current_img()[0]), len(history.get_current_img()))        
    
    def update_img_preview(label: tk.Label):
        current_image = history.get_current_img().copy()
        if using_selection:
            current_image = apply_marching_ants_border(current_image, selection, (len(current_image[0]), len(current_image)))
        new_image = Image.fromarray(current_image)
        new_tk_image = ImageTk.PhotoImage(new_image)
        # update the image label
        label.config(image=new_tk_image)
        # prevent garbage collector from deleting image?
        label.image = new_tk_image

        
    def img_operation(func, *args):
        if using_selection:
            current_whole = history.get_current_img()
            current_selection = current_whole[selection[0][1]:selection[1][1], selection[0][0]:selection[1][0]]
            # perform the operation (on the selection area)
            edited_selection = func(current_selection, *args)
            current_whole[selection[0][1]:selection[1][1], selection[0][0]:selection[1][0]] = edited_selection
        else:
            current_whole = func(history.get_current_img(), *args)
        # add it to the history
        history.add_record(current_whole)
        update_img_preview(img_preview)
        
    # store temporary bindings in a dictionary so we can reference them for unbinding
    bindings = {}
        
    # selection tool
    # TODO: clamp to image bounds
    selection_button = tk.Button(text="Select Area")
    # click event
    def begin_selection(event):
        """Defines the starting point for the selection"""
        # first reset the selection area
        reset_selection()
        selection[0] = (event.x, event.y)
        # print("begin selection:", selection)
    # drag event
    def making_selection(event):
        """Dynamically update selection area while mouse is dragging"""
        if event.x != selection[0][1] and event.y != selection[0][0]:
            # assign coordinate and clamp if we are outside image bounds
            selection[1] = (min(event.x + 1, len(history.get_current_img()[0])), min(event.y + 1, len(history.get_current_img())))
            update_img_preview(img_preview)
            # print("dragging selection:", selection)
    # released event
    def released_selection(event):
        """Mouse is released; verify and apply selection"""
        if event.x == selection[0][1] and event.y == selection[0][0]:
            print("No pixels selected, resetting selection")
            selection[0] = (0,0)
            selection[1] = (len(history.get_current_img()[0]), len(history.get_current_img()))
        else:
            # assign coordinate and clamp if we are outside image bounds
            selection[1] = (min(event.x + 1, len(history.get_current_img()[0])), min(event.y + 1, len(history.get_current_img())))
            # print(f"\nraw selection: {selection[0]} to ({event.x+1}, {event.y+1})")
            normalized = normalize_coord_pair(selection[0], selection[1])
            selection[0] = normalized[0]
            selection[1] = normalized[1]
            # print(f"\nending selection: {selection[0]} to {selection[1]}")
            update_img_preview(img_preview)
    # control the button's behavior
    def toggle_selection():
        """Control selection tool button"""
        nonlocal using_selection
        using_selection = not using_selection
        if using_selection:
            selection_button.config(text="Cancel Selection")
            # bind temporary event listeners
            bindings["begin_selection"] = img_preview.bind("<ButtonPress-1>", begin_selection)
            bindings["making_selection"] = img_preview.bind("<B1-Motion>", making_selection)
            bindings["released_selection"] = img_preview.bind("<ButtonRelease-1>", released_selection)
        else:
            selection_button.config(text="Select Area")
            # unbind unused event listeners (not sure if this is really necessary but whatever)
            img_preview.unbind("<begin_selection-1>", bindings["begin_selection"])
            bindings.pop("begin_selection")
            img_preview.unbind("<B1-Motion>", bindings["making_selection"])
            bindings.pop("making_selection")
            img_preview.unbind("<ButtonRelease-1>", bindings["released_selection"])
            bindings.pop("released_selection")
            # update preview to remove selection box
            update_img_preview(img_preview)
    selection_button.config(command=toggle_selection)
    
    # button = tk.Button(text="Cancel selection" if using_selection else "Select Area", command=toggle_selection)
    selection_button.pack()

    for buttonData in img_operation_buttons:
        if len(buttonData) <= 2:
            # function is a lambda so that it can take arguments
            # "func=" thing is to save the current value within the loop; otherwise it would check buttonData[1] upon execution
            button = tk.Button(text=buttonData[0], command=lambda func=buttonData[1]: img_operation(func))
        else:
            # function has multiple args
            button = tk.Button(text=buttonData[0], command=lambda func=buttonData[1], args=buttonData[2]: img_operation(func, args))
        button.pack()
    
    
    image_path_noext = sys.argv[1][0:sys.argv[1].find(".")]
    image_ext = sys.argv[1][sys.argv[1].find("."):len(sys.argv[1])]
    image_path = image_path_noext + "_edit" + image_ext
    button = tk.Button(text="Save Copy", command=lambda: save_image(history.get_current_img(), image_path))
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
    # history.add_record(load_image("nyx.png"))
    
    # display the window
    gui(history)

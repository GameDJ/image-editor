import tkinter as tk
from typing import Callable
from enum import Enum
from Image import Image
import PIL.Image
from Arguments import Arguments
import PIL
from PIL import ImageTk
from GUI_Defaults import GUI_Defaults
from ImageMode import ImageMode

class Image_GUI():
    def __init__(self, parent_frame: tk.Frame, handler_get_render_image: Callable[[], Image]):
        # Outside refs
        self._handler_get_render_image = handler_get_render_image

        # image preview frame
        self.image_frame = tk.Frame(parent_frame, width=400, height=300, background="#000000", borderwidth=1)
        self.image_frame.grid(row=0, column=0, rowspan=3, columnspan=3, padx=3, pady=3, sticky="nsew")
        parent_frame.grid_rowconfigure(0, minsize=300, weight=1)
        parent_frame.grid_columnconfigure(0, minsize=400, weight=1)

        # a label to hold the image
        self.image_preview = tk.Label(self.image_frame, borderwidth=0, cursor=GUI_Defaults.CURSOR.value)
        # img_preview.pack(side=tk.TOP)
        # img_preview.grid(sticky="nsew")
        self.image_preview.place(in_=self.image_frame, anchor="c", relx=.5, rely=.5)

        self.loaded_file_name = "image.png"

    def refresh_image(self, args: Arguments = None):
        """Regenerate the image preview from the render image provided by RequestHandler.  
        Arguments:
        args -- draw a temporary shape if one is provided"""
        new_pil_image = PIL.Image.fromarray(self._handler_get_render_image(args).get_img_array())
        new_tk_image = ImageTk.PhotoImage(new_pil_image)
        # update the image label
        self.image_preview.config(image=new_tk_image)
        # prevent garbage collector from deleting image...?
        self.image_preview.image = new_tk_image

    def change_image_mode(self, toggle_on: Callable = None, toggle_off: Callable = None):
        """Change the image mode and turn off the action previously in use, if any"""
        
        is_same_mode = False

        if hasattr(self, "toggle_image_mode_off"):
            # if we have a stored toggle_of action (i.e. there is an active binding)
            self.toggle_image_mode_off()
            if toggle_off == self.toggle_image_mode_off:
                # new is same mode as current; don't toggle it back on
                is_same_mode = True
                # reset the cursor to default
                self.image_preview.config(cursor=GUI_Defaults.CURSOR.value)
            del self.toggle_image_mode_off

        if not is_same_mode:
            toggle_on()
            # set the toggle off method to be called next time
            self.toggle_image_mode_off = toggle_off
            # change the cursor to the active style
            self.image_preview.config(cursor=GUI_Defaults.CURSOR_IMG_ACTION.value)

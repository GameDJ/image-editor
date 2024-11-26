import tkinter as tk
from tkinter import font, colorchooser
from typing import Callable
from enum import Enum
import numpy as np
import os

class Color_GUI(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, gui_defaults: Enum, gui_change_image_mode: Callable, handler_get_color_at_pixel: Callable, gui_bindings: dict, gui_image_preview: tk.Label, gui_refresh_image: Callable):
        # Outside refs
        self._gui_defaults = gui_defaults
        self._gui_change_image_mode = gui_change_image_mode
        self._handler_get_color_at_pixel = handler_get_color_at_pixel
        self._gui_bindings = gui_bindings
        self._gui_image_preview = gui_image_preview
        self._gui_refresh_image = gui_refresh_image
        
        self.color = (255, 0, 0)
        
        # Selection panel frame
        self.frame = tk.Frame(parent_frame)
        # Label
        self.label = tk.Label(self.frame, text="Color", font=self._gui_defaults.PANEL_TITLE_FONT.value)
        self.label.pack(side = tk.TOP)
        
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack(side=tk.TOP)
        
        # Color preview button
        self.fakeimage = tk.PhotoImage(width=1, height=1)
        self.color_preview = tk.Button(self.btn_frame, text="", image=self.fakeimage, width=24, height=24, compound="c", command=self._change_color, background=self._convert_color_to_hex(self.color), relief="groove")
        self.color_preview.grid(row=0, column=1, padx=3)
        self._update_color()
        
        # Eyedropper button
        self.eyedrop_img = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), r"..\assets\icons8-color-dropper-24.png"))
        self.eyedropper_btn = tk.Button(self.btn_frame, command=self._gui_change_image_mode, relief=self._gui_defaults.BUTTON_RELIEF.value, image=self.eyedrop_img)
        # eyedropper_btn.pack(side=tk.TOP)
        self.eyedropper_btn.grid(row=0, column=3, padx=3)
        
    def _convert_color_to_hex(self, rgb: np.ndarray):
        return "#%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])
    
    def _change_color(self):
        color = colorchooser.askcolor(title="Choose color", initialcolor=self._convert_color_to_hex(self.color))
        if all(color):
            # print(color)
            self.color = color[0]
            self._update_color()
            
    def _update_color(self):
        self.color_preview.config(background=self._convert_color_to_hex(self.color))
        
    def select_pixel_color(self, event: tk.Event):
        self.color = self._handler_get_color_at_pixel(event.x, event.y)
        self._update_color()
        
    def toggle_eyedropper_on(self):
        self._gui_bindings["select_pixel_color"] = self._gui_image_preview.bind("<ButtonPress-1>", self.select_pixel_color)
        self.eyedropper_btn.config(relief=self._gui_defaults.BUTTON_TOGGLED_RELIEF.value)
        
    def toggle_eyedropper_off(self):
        self._gui_image_preview.unbind("<begin_selection-1>", self._gui_bindings["select_pixel_color"])
        self._gui_bindings.pop("select_pixel_color")
        self.eyedropper_btn.config(relief=self._gui_defaults.BUTTON_RELIEF.value)
import os
import tkinter as tk
from tkinter import font, colorchooser
from typing import Callable
from Classes.gui.GUI_Defaults import GUI_Defaults
from Classes.gui.assets.eyedropper import image_string

class Color_GUI():
    def __init__(self, parent_frame: tk.Frame, gui_title_font: font, gui_change_image_mode: Callable, handler_get_color_at_pixel: Callable, gui_bindings: dict, gui_image_preview: tk.Label, gui_refresh_image: Callable):
        # Outside refs
        self._gui_change_image_mode = gui_change_image_mode
        self._handler_get_color_at_pixel = handler_get_color_at_pixel
        self._gui_bindings = gui_bindings
        self._gui_image_preview = gui_image_preview
        self._gui_refresh_image = gui_refresh_image
        
        self.color_codes = ((255, 0, 0), "#ff0000")
        
        # Selection panel frame
        self.frame = tk.Frame(parent_frame)
        # Label
        self.label = tk.Label(self.frame, text="Color", font=gui_title_font)
        self.label.pack(side = tk.TOP)
        
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack(side=tk.TOP)
        
        # Color preview button
        self._fakeimage = tk.PhotoImage(width=1, height=1)
        self.color_preview = tk.Button(self.btn_frame, text="", image=self._fakeimage, width=24, height=24, compound="c", command=self._change_color, background=self.color_codes[1], relief="groove")
        self.color_preview.grid(row=0, column=1, padx=3)
        self._update_color()
        
        # Eyedropper button
        # self.eyedrop_img = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), r"..\..\assets\icons8-color-dropper-24.png"))
        self.eyedrop_img = tk.PhotoImage(data=image_string)
        self.eyedropper_btn = tk.Button(self.btn_frame, command=lambda: self._gui_change_image_mode(self.toggle_eyedropper_on, self.toggle_eyedropper_off), relief=GUI_Defaults.BUTTON_RELIEF.value, image=self.eyedrop_img)
        # eyedropper_btn.pack(side=tk.TOP)
        self.eyedropper_btn.grid(row=0, column=3, padx=3)
        
    def _convert_color_to_hex(self, rgb: tuple[int, int, int]):
        return "#%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])
    
    def _change_color(self):
        new_color_codes = colorchooser.askcolor(title="Choose color", initialcolor=self.color_codes[1])
        if all(new_color_codes):
            # print(color)
            self.color_codes = new_color_codes
            self._update_color()
            
    def _update_color(self):
        self.color_preview.config(background=self.color_codes[1])
        
    def select_pixel_color(self, event: tk.Event):
        color_RGB = self._handler_get_color_at_pixel(event.x, event.y)
        self.color_codes = (color_RGB, self._convert_color_to_hex(color_RGB))
        self._update_color()
        
    def toggle_eyedropper_on(self):
        self._gui_bindings[GUI_Defaults.CLICK_PRESS_BINDING] = self._gui_image_preview.bind(GUI_Defaults.CLICK_PRESS_BINDING.value, self.select_pixel_color)
        self.eyedropper_btn.config(relief=GUI_Defaults.BUTTON_TOGGLED_RELIEF.value)
        
    def toggle_eyedropper_off(self):
        self._gui_image_preview.unbind(GUI_Defaults.CLICK_PRESS_BINDING.value, self._gui_bindings.pop(GUI_Defaults.CLICK_PRESS_BINDING))
        self.eyedropper_btn.config(relief=GUI_Defaults.BUTTON_RELIEF.value)
        
    def get_color_codes(self):
        return self.color_codes
    
    def toggle_buttons(self, toggle_on: bool):
        state = "active" if toggle_on else "disabled"
        
        self.eyedropper_btn.config(state=state)
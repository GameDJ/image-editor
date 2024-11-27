import tkinter as tk
from tkinter import font
from typing import Callable
from Selection import Selection
from enum import Enum
from tkinter import font
from GUI_Defaults import GUI_Defaults

class Selection_GUI():
    def __init__(self, parent_frame: tk.Frame, gui_title_font: font, gui_change_image_mode: Callable, handler_make_selection: Callable, handler_get_selection_bbox: Callable, handler_clear_selection: Callable, handler_get_image_dimensions: Callable, gui_bindings: dict, gui_image_preview: tk.Label, gui_refresh_image: Callable):
        # Constants
        self._SEL_COORD_1_DEFAULT_TEXT = "No selection"
        
        # Outside refs
        self._gui_change_image_mode = gui_change_image_mode
        self._handler_make_selection = handler_make_selection
        self._handler_get_selection_bbox = handler_get_selection_bbox
        self._handler_clear_selection = handler_clear_selection
        self._handler_get_image_dimensions = handler_get_image_dimensions
        self._gui_bindings = gui_bindings
        self._gui_image_preview = gui_image_preview
        self._gui_refresh_image = gui_refresh_image
        
        # Selection panel frame
        self.frame = tk.Frame(parent_frame)
        # Label
        self.label = tk.Label(self.frame, text="Selection", font=gui_title_font)
        self.label.pack(side = tk.TOP)
        # Frame for history buttons
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack(side=tk.TOP)
        # Select & Clear buttons
        self.select_btn = tk.Button(self.btn_frame, text="Select", command=lambda: self._gui_change_image_mode(self.toggle_select_on, self.toggle_select_off), underline=0)
        self.select_btn.grid(column=0, row=0)
        self.clear_btn = tk.Button(self.btn_frame, text="Clear", command=self.clear_selection, state="disabled", underline=0)
        self.clear_btn.grid(column=1, row=0)
        # coordinate display
        self.sel_coord_1 = tk.Label(self.frame, text=self._SEL_COORD_1_DEFAULT_TEXT)
        self.sel_coord_1.pack()
        self.sel_coord_2 = tk.Label(self.frame, text="")
        self.sel_coord_2.pack()

    def toggle_select_on(self):
        self._gui_bindings[GUI_Defaults.CLICK_PRESS_BINDING] = self._gui_image_preview.bind(GUI_Defaults.CLICK_PRESS_BINDING.value, self._begin_selection)
        self._gui_bindings[GUI_Defaults.CLICK_DRAG_BINDING] = self._gui_image_preview.bind(GUI_Defaults.CLICK_DRAG_BINDING.value, self._making_selection)
        self._gui_bindings[GUI_Defaults.CLICK_RELEASE_BINDING] = self._gui_image_preview.bind(GUI_Defaults.CLICK_RELEASE_BINDING.value, self._released_selection)
        self.select_btn.config(relief=GUI_Defaults.BUTTON_TOGGLED_RELIEF.value)
    
    def toggle_select_off(self):
        self._gui_image_preview.unbind(GUI_Defaults.CLICK_PRESS_BINDING.value, self._gui_bindings.pop(GUI_Defaults.CLICK_PRESS_BINDING))
        self._gui_image_preview.unbind(GUI_Defaults.CLICK_DRAG_BINDING.value, self._gui_bindings.pop(GUI_Defaults.CLICK_DRAG_BINDING))
        self._gui_image_preview.unbind(GUI_Defaults.CLICK_RELEASE_BINDING.value, self._gui_bindings.pop(GUI_Defaults.CLICK_RELEASE_BINDING))
        self.select_btn.config(relief=GUI_Defaults.BUTTON_RELIEF.value)

    def _begin_selection(self, event: tk.Event):
        self.clear_selection()
        self.start_coord = (event.x, event.y)
    
    def _making_selection(self, event: tk.Event):
        # verify coord is within the image bounds
        image_dimensions = self._handler_get_image_dimensions()
        x_clamped = min(max(0, event.x), image_dimensions[1]-1)
        y_clamped = min(max(0, event.y), image_dimensions[0]-1)
        
        self._handler_make_selection(self.start_coord, (x_clamped, y_clamped))
        self._update_coord_display()
        self._gui_refresh_image()
        
    def _calc_coord_display_text(self, x: int, y: int) -> str:
        return f"x: {x}, y: {y}"
        
    def _update_coord_display(self):
        bbox = self._handler_get_selection_bbox()
        self.sel_coord_1.config(text=f"x: {bbox[0]}, y: {1}")
        self.sel_coord_2.config(text=f"x: {bbox[2]}, y: {3}")

    def _released_selection(self, event: tk.Event):
        if self._handler_get_selection_bbox() is not None:
            self._gui_refresh_image()
            self.clear_btn.config(state="active")
        
    def clear_selection(self, *_):
        if hasattr(self, "start_coord"):
            del self.start_coord
        if hasattr(self, "end_coord"):
            del self.end_coord
        cleared = self._handler_clear_selection()
        if cleared:
            self.clear_btn.config(state="disabled")
            self.sel_coord_1.config(text=self._SEL_COORD_1_DEFAULT_TEXT)
            self.sel_coord_2.config(text="")
            self._gui_refresh_image()
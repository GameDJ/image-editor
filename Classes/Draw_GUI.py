import tkinter as tk
from typing import Callable
from enum import Enum

class Draw_GUI(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, gui_defaults: Enum, gui_change_image_mode: Callable, handler_get_image_dimensions: Callable, gui_bindings: dict, gui_image_preview: tk.Label, gui_refresh_image: Callable):
        # Outside refs
        self._gui_defaults = gui_defaults
        self._gui_change_image_mode = gui_change_image_mode
        self._handler_get_image_dimensions = handler_get_image_dimensions
        self._gui_bindings = gui_bindings
        self._gui_image_preview = gui_image_preview
        self._gui_refresh_image = gui_refresh_image
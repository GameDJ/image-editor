import tkinter as tk
from tkinter import font
from typing import Callable
from Defaults import Defaults

class Selection_GUI(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, change_image_mode: Callable, handler_make_selection: Callable, handler_get_selection: Callable, handler_clear_selection: Callable, gui_bindings: dict, gui_image_preview: tk.Label, gui_refresh_image: Callable):
        # Outside refs
        self._handler_make_selection = handler_make_selection
        self._handler_get_selection = handler_get_selection
        self._handler_clear_selection = handler_clear_selection
        self._gui_bindings = gui_bindings
        self._gui_image_preview = gui_image_preview
        self._gui_refresh_image = gui_refresh_image
        
        # Selection frame
        self.frame = tk.Frame(parent_frame)
        # Label
        self.label = tk.Label(self.frame, text="Selection", font=Defaults.PANEL_TITLE_FONT)
        self.label.pack(side = tk.TOP)
        # Frame for history buttons
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack(side=tk.TOP)
        # Select & Clear buttons
        self.select_btn = tk.Button(self.btn_frame, text="Select", command=change_image_mode)
        self.select_btn.grid(column=0, row=0)
        self.clear_btn = tk.Button(self.btn_frame, text="Clear", command=self.redo, state="disabled")
        self.clear_btn.grid(column=1, row=0)

    def toggle_select_on(self):
            self._gui_bindings["begin_selection"] = self._gui_image_preview.bind("<ButtonPress-1>", self.begin_selection)
            self._gui_bindings["making_selection"] = self._gui_image_preview.bind("<B1-Motion>", self.making_selection)
            self._gui_bindings["released_selection"] = self._gui_image_preview.bind("<ButtonRelease-1>", self.released_selection)
    
    def toggle_select_off(self):
            self._gui_image_preview.unbind("<begin_selection-1>", self._gui_bindings.pop("begin_selection"))
            self._gui_image_preview.unbind("<B1-Motion>", self._gui_bindings.pop("making_selection"))
            self._gui_image_preview.unbind("<ButtonRelease-1>", self._gui_bindings.pop("released_selection"))

    def begin_selection(self):
        pass
    
    def making_selection(self):
        pass

    def finalize_selection(self):
        self._gui_refresh_image()
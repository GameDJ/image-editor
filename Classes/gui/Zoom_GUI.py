import tkinter as tk
from typing import Callable
from enum import Enum
from tkinter import font

class Zoom_GUI():
    def __init__(self, parent_frame: tk.Frame, gui_title_font: font, handler_zoom_change: Callable, handler_get_zoom_level: Callable, gui_toggle_actions_while_zoomed: Callable, refresh_image: Callable):
        # Outside refs
        self._handler_zoom_change = handler_zoom_change
        self._handler_get_zoom_level = handler_get_zoom_level
        self._gui_toggle_actions_while_zoomed = gui_toggle_actions_while_zoomed
        self._gui_refresh_image = refresh_image
        
        # Zoom panel frame
        self.frame = tk.Frame(parent_frame)
        # Label
        self.label = tk.Label(self.frame, text="Zoom", font=gui_title_font)
        self.label.pack(side = tk.TOP)
        # Frame for inner buttons
        self.inner_frame = tk.Frame(self.frame)
        self.inner_frame.pack(side=tk.TOP)
        
        self.zoom_level = 1.0

        # fake image for controlling exact size of the buttons
        self._fakeimage = tk.PhotoImage(width=1, height=1)
        
        self.zoom_out_btn = tk.Button(self.inner_frame, text="-", command=lambda: self.zoom_change(-1), image=self._fakeimage, compound="c", width=20, height=20, state="disabled")
        self.zoom_out_btn.pack(side=tk.LEFT, padx=1)
        
        self.zoom_level_label = tk.Label(self.inner_frame, text=f"1x")
        self.zoom_level_label.pack(side=tk.LEFT, padx=3)
        
        self.zoom_in_btn = tk.Button(self.inner_frame, text="+", command=lambda: self.zoom_change(1), image=self._fakeimage, compound="c", width=20, height=20, state="disabled")
        self.zoom_in_btn.pack(side=tk.LEFT, padx=1)

    def zoom_change(self, delta: int):
        self._handler_zoom_change(delta)
        self.refresh_zoom()
        
    def toggle_buttons(self, toggle_on: bool):
        state = "active" if toggle_on else "disabled"
        self.zoom_out_btn.config(state=state)
        self.zoom_in_btn.config(state=state)
        
    def refresh_zoom(self):
        self.zoom_level = self._handler_get_zoom_level()
        
        if self.zoom_level < 0:
            zoom_text = f"1/{abs(int(self.zoom_level)-1)}x"
        else:
            zoom_text = f"{int(self.zoom_level)}x"
        self.zoom_level_label.config(text=zoom_text)
        self._gui_refresh_image()
        
        # disable certain actions while zoomed
        if self.zoom_level != 1:
            self._gui_toggle_actions_while_zoomed(False)
        else:
            self._gui_toggle_actions_while_zoomed(True)
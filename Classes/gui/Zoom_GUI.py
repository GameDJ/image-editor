import tkinter as tk
from typing import Callable
from enum import Enum
from tkinter import font

class Zoom_GUI():
    def __init__(self, parent_frame: tk.Frame, gui_title_font: font, handler_zoom_change: Callable, refresh_image: Callable):
        # Outside refs
        self._handler_zoom_change = handler_zoom_change
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
        
        self.zoom_out_btn = tk.Button(self.inner_frame, text="-", command=lambda: self.zoom_change(-1), image=self._fakeimage, compound="c", width=20, height=20)
        self.zoom_out_btn.pack(side=tk.LEFT, padx=1)
        
        self.zoom_level_label = tk.Label(self.inner_frame, text=f"1x")
        self.zoom_level_label.pack(side=tk.LEFT, padx=3)
        
        self.zoom_in_btn = tk.Button(self.inner_frame, text="+", command=lambda: self.zoom_change(1), image=self._fakeimage, compound="c", width=20, height=20)
        self.zoom_in_btn.pack(side=tk.LEFT, padx=1)

    def zoom_change(self, delta: int):
        self.zoom_level = self._handler_zoom_change(delta)
        if self.zoom_level < 0:
            self.zoom_level_label.config(text=f"1/{2**(int(self.zoom_level)*-1)}x")
        else:
            self.zoom_level_label.config(text=f"{int(self.zoom_level)}x")
        self._gui_refresh_image()
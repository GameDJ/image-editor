import tkinter as tk
from tkinter import simpledialog, colorchooser

class CanvasDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, color_codes=((255, 0, 0), "#ff0000"), use_color=True):
        self.width = None
        self.height = None
        self.use_color = use_color
        if use_color:
            self.color_codes = color_codes
        super().__init__(parent, title=title)
        
    def body(self, master):
        tk.Label(master, text="Width:").grid(row=0, column=0, padx=5, pady=5)
        self.width_entry = tk.Entry(master)
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Height:").grid(row=1, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)
        
        if self.use_color:
            tk.Label(master, text="Color:").grid(row=2, column=0, padx=5, pady=5)
            self._fakeimage = tk.PhotoImage(width=1, height=1)
            self.color_btn = tk.Button(master, text="", image=self._fakeimage, width=16, height=16, compound="c", command=self.choose_color, background=self.color_codes[1], relief="groove")
            self.color_btn.grid(row=2, column=1, padx=5, pady=5)

        return self.width_entry  # Initial focus
    
    def choose_color(self):
        new_color_codes = colorchooser.askcolor(title="Choose Color")
        if all(new_color_codes):
            self.color_codes = new_color_codes
            self.color_btn.config(bg=new_color_codes[1])
            
    def apply(self):
        try:
            self.width = int(self.width_entry.get())
            self.height = int(self.height_entry.get())
        except ValueError:
            self.width = self.height = None  # Reset if invalid
        # Color is already set by `choose_color`
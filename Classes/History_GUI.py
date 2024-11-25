import tkinter as tk
from tkinter import font
from typing import Callable
from enum import Enum

class History_GUI(tk.Frame):
    def __init__(self, parent_frame: tk.Frame, gui_defaults: Enum, handler_undo: Callable, handler_redo: Callable, handler_history_get_index: Callable, handler_history_set_index: Callable, handler_history_descriptions: Callable, refresh_image: Callable):
        # Outside refs
        self._gui_defaults = gui_defaults
        self._handler_undo = handler_undo
        self._handler_redo = handler_redo
        self._handler_history_get_index = handler_history_get_index
        self._handler_history_set_index = handler_history_set_index
        self._handler_history_descriptions = handler_history_descriptions
        self._gui_refresh_image = refresh_image
        
        # History panel frame
        self.frame = tk.Frame(parent_frame)
        # Label
        self.label = tk.Label(self.frame, text="History", font=gui_defaults.PANEL_TITLE_FONT)
        self.label.pack(side = tk.TOP)
        # Frame for history buttons
        self.btn_frame = tk.Frame(self.frame)
        self.btn_frame.pack(side=tk.TOP)
        # Undo & Redo buttons
        self.undo_btn = tk.Button(self.btn_frame, text="Undo", command=self.undo, state="disabled")
        self.undo_btn.grid(column=0, row=0)
        self.redo_btn = tk.Button(self.btn_frame, text="Redo", command=self.redo, state="disabled")
        self.redo_btn.grid(column=1, row=0)
        # Listbox
        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(padx=1, pady=1)
        self.listbox.bind("<<ListboxSelect>>", self._history_clicked)
        
    def undo(self, *_):
        # update data
        self._handler_undo()
        # update ui
        self._gui_refresh_image()
        self.refresh_history()
        
    def redo(self, *_):
        self._handler_redo()
        self._gui_refresh_image()
        self.refresh_history()
        
    def refresh_history(self):
        """Regenerate the history list based on the history given by RequestHandler"""
        # clear the current entries (in the UI)
        self.listbox.delete(0, tk.END)
        # repopulate the listbox
        entry_descs = self._handler_history_descriptions()
        for entry_desc in entry_descs:
            self.listbox.insert(tk.END, entry_desc[1])
        # underline the currently selected history entry
        self.listbox.activate(self._handler_history_get_index())
        self.listbox.focus()
        # determine whether undo and redo are clickable given the current state
        if self._handler_history_get_index() <= 0:
            # first entry is selected; no more undo
            self.undo_btn.config(state="disabled")
        else:
            self.undo_btn.config(state="active")
        if self._handler_history_get_index() >= len(entry_descs)-1:
            # latest entry is selected; can't redo
            self.redo_btn.config(state="disabled")
        else:
            self.redo_btn.config(state="active")
            
    def _history_clicked(self, _):
        """Set the history index based on a mouse click"""
        if len(self.listbox.curselection()) > 0:
            self._handler_history_set_index(self.listbox.curselection()[0])
            self.refresh_history()
            self._gui_refresh_image()
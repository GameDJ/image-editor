import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, filedialog
from typing import Callable
from Classes.edit.filter.FilterType import FilterInfo
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType
from Classes.gui.CanvasDialog import CanvasDialog

class Menubar_GUI():
    def __init__(self, root: tk.Tk, handler_create_canvas: Callable, handler_import_image: Callable, handler_export_image: Callable, handler_get_file_path: Callable, handler_is_active_image: Callable, handler_edit: Callable, gui_get_color_codes: Callable, gui_refresh_history: Callable, gui_refresh_image: Callable):
        # outside refs
        self._root = root
        self._handler_create_canvas = handler_create_canvas
        self._handler_import_image = handler_import_image
        self._handler_export_image = handler_export_image
        self._handler_get_file_path = handler_get_file_path
        self._handler_is_active_image = handler_is_active_image
        self._handler_edit = handler_edit
        self._gui_get_color_codes = gui_get_color_codes
        self._gui_refresh_image = gui_refresh_image
        self._gui_refresh_history = gui_refresh_history

        self.menubar = tk.Menu(root, title="Menubar")

        self.structure = {
            "File": {
                "Create blank canvas": lambda: self.create_canvas(),
                "Load": lambda: self.load_file(),
                "Save as": lambda: self.save_file()
            },
            "Edit": { 
                "Filter": {
                    # populate the commands based on available filters
                    FilterInfo[filter]["text"]:lambda filter=filter: self.filter_action(filter) for filter in FilterInfo
                },
                "Resize": lambda: self.resize()
            },
            "About": lambda: self.display_help_message("SIMPLE v1.0.0", "SIMPLE: Simple IMage Processor for Lazy Editors\n\nContributors:\n\tAddison Casner\n\tDerek Jennings\n\tQuinn Pulley\n\tWill Verplaetse")
        }

        self.menu_storage = {self.menubar: {}}
        for submenu in self.structure:
            self.generate_menu(self.menubar, self.menu_storage[self.menubar], submenu, self.structure[submenu])
    

    def generate_menu(self, parent_menu: tk.Menu, parent_obj: dict, cur_key: str, cur_level_obj):
        """Recursively generate a nested menu.
        Designed to store the menus in a nested dictionary, though it's not necessary.
        
        Args:
        parent_menu -- parent menu (which can be a key)
        parent_obj -- a dict (which can be the value associated with parent_menu)
        cur_key -- a key in the source dict
        cur_level_obj -- the value (a dict or function) associated with cur_key in the source dict
        """
        if type(cur_level_obj) is dict:
            # add a submenu
            new_submenu = tk.Menu(parent_menu, tearoff=0)
            parent_obj[new_submenu] = {}
            parent_menu.add_cascade(label=cur_key, menu=new_submenu)
            # generate each menu (or command) nested inside this one
            for next_level_key in cur_level_obj:
                self.generate_menu(new_submenu, parent_obj[new_submenu], next_level_key, cur_level_obj[next_level_key])
        else:
            # add a command
            parent_menu.add_command(label=cur_key, command=cur_level_obj)

    def display_help_message(self, title: str, text: str):
        messagebox.showinfo(title=title, message=text)


    def create_canvas(self):
        if self._handler_is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
            
        canvasDialog = CanvasDialog(self._root, title="Initialize Canvas", color_codes=self._gui_get_color_codes())
        if not canvasDialog.width or not canvasDialog.height:
            messagebox.showerror(title="Operation cancelled", message="Failed to create canvas")
        else:
            self._handler_create_canvas(canvasDialog.width, canvasDialog.height, canvasDialog.color_codes[0])
            self._gui_refresh_image()
            # activate_savebtn()
            self._gui_refresh_history()
    
    def load_file(self):
        if self._handler_is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
        loaded_file_name = filedialog.askopenfilename(title="Select a file")
        if not loaded_file_name:
            messagebox.showerror(title="Operation cancelled", message="No file selected")
            return
        if not self._handler_import_image(loaded_file_name):
            messagebox.showerror(title="Operation cancelled", message="Failed to load image")
            return
        self._gui_refresh_image()
        # activate_savebtn()
        self._gui_refresh_history()
        
    def save_file(self):
        if self._handler_is_active_image() is not None:
            file_path = self._handler_get_file_path()
            if file_path is None:
                file_path = ""
            file_name = file_path.split("/")[-1]
            file_dir = file_path[len(file_name):]
            path = filedialog.asksaveasfilename(title="Save as:", initialdir=file_dir, initialfile=file_name, defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if path is not None:
                self._handler_export_image(path)
            # should check to see if the file exists now, to verify it saved
            #
        else:
            messagebox.showerror(title="Error", message="No image loaded")

    def filter_action(self, filter):
        args = Arguments()
        args.add_filter(filter)
        for arg in FilterInfo[filter]["args"]:
            if arg == ArgumentType.AMOUNT:
                args.add_amount(simpledialog.askfloat(title="Amount entry", prompt="Enter amount:"))
            elif arg == ArgumentType.COLOR:
                args.add_color(colorchooser.askcolor(title="Choose a color")[1])
        # handler will add image and selection to args before passing it to the edit class
        try:
            self._handler_edit(args)
            self._gui_refresh_history()
            self._gui_refresh_image()
        except ValueError:
            messagebox.showerror("Error", "Invalid value")

    def resize(self):
        print("dialog goes here")
        print("resize")
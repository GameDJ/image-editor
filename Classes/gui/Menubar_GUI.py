import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, filedialog
from typing import Callable
from Classes.edit.filter.FilterType import FilterInfo
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType
from Classes.gui.CanvasDialog import CanvasDialog
from Classes.gui.GUI_Defaults import GUI_Defaults

class Menubar_GUI():
    def __init__(self, root: tk.Tk, handler_create_canvas: Callable, handler_import_image: Callable, handler_export_image: Callable, handler_get_file_path: Callable, handler_is_active_image: Callable, handler_edit: Callable, handler_resize: Callable, gui_clear_selection: Callable, gui_get_color_codes: Callable, gui_refresh_history: Callable, gui_refresh_image: Callable, gui_refresh_zoom: Callable, gui_toggle_buttons: Callable):
        # outside refs
        self._root = root
        self._handler_create_canvas = handler_create_canvas
        self._handler_import_image = handler_import_image
        self._handler_export_image = handler_export_image
        self._handler_get_file_path = handler_get_file_path
        self._handler_is_active_image = handler_is_active_image
        self._handler_edit = handler_edit
        self._handler_resize = handler_resize
        self._gui_clear_selection = gui_clear_selection
        self._gui_get_color_codes = gui_get_color_codes
        self._gui_refresh_image = gui_refresh_image
        self._gui_refresh_history = gui_refresh_history
        self._gui_refresh_zoom = gui_refresh_zoom
        self._gui_toggle_buttons = gui_toggle_buttons

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
            "Help": {
                "Keybinds": lambda: self.display_keybinds(),
                "About": lambda: self.display_about_message()
            }
        }

        # "File": (menu, {"Open": command}),
        # "Edit": (menu, {"Filter": (menu, {"Blur": command})})
        self.menu_storage = {self.menubar: {}}
        for submenu in self.structure:
            self.generate_menu(self.menubar, self.menu_storage[self.menubar], submenu, self.structure[submenu])
        self.toggle_buttons(False)


    def generate_menu(self, parent_menu: tk.Menu, parent_obj: dict, cur_key: str, cur_level_obj):
        """Recursively generate a nested menu.
        Designed to store the menus in a nested dictionary, though it's not necessary.
        Format: "Edit": (editmenu, {"Filter": (filtermenu, {"Blur": command})})
        
        Args:
        parent_menu -- parent menu (which can be a key)
        parent_obj -- a dict (which can be the value associated with parent_menu)
        cur_key -- a key in the source dict
        cur_level_obj -- the value (a dict or function) associated with cur_key in the source dict
        """
        if type(cur_level_obj) is dict:
            # add a submenu
            new_submenu = tk.Menu(parent_menu, tearoff=0)
            parent_menu.add_cascade(label=cur_key, menu=new_submenu)
            parent_obj[cur_key] = (new_submenu, {})
            # generate each menu (or command) nested inside this one
            for next_level_key in cur_level_obj:
                self.generate_menu(new_submenu, parent_obj[cur_key][1], next_level_key, cur_level_obj[next_level_key])
        else:
            # add a command
            parent_menu.add_command(label=cur_key, command=cur_level_obj)
            parent_obj[cur_key] = cur_level_obj

    def display_help_message(self, title: str, text: str):
        messagebox.showinfo(title=title, message=text)

    def create_canvas(self):
        if self._handler_is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
            
        canvasDialog = CanvasDialog(self._root, title="Initialize Canvas", color_codes=self._gui_get_color_codes())
        if canvasDialog.width and canvasDialog.height:
            shrunk = False
            if canvasDialog.width > GUI_Defaults.IMAGE_MAX_WIDTH.value:
                canvas_width = GUI_Defaults.IMAGE_MAX_WIDTH.value
                shrunk = True
            else:
                canvas_width = canvasDialog.width
            if canvasDialog.height > GUI_Defaults.IMAGE_MAX_HEIGHT.value:
                canvas_height = GUI_Defaults.IMAGE_MAX_HEIGHT.value
                shrunk = True
            else:
                canvas_height = canvasDialog.height
            if shrunk:
                messagebox.showwarning(title="Operation modified", message=f"Image shrunk to fit max bounds of {GUI_Defaults.IMAGE_MAX_WIDTH.value}x{GUI_Defaults.IMAGE_MAX_HEIGHT.value}.\nNew dimensions: {canvas_width}x{canvas_height}")

            try:
                self._handler_create_canvas(canvasDialog.width, canvasDialog.height, canvasDialog.color_codes[0])
            except ValueError:
                messagebox.showerror(title="Operation cancelled", message="Invalid value entered")
                return
            self._gui_refresh_image()
            self._gui_refresh_history()
            self._gui_refresh_zoom()
            self.toggle_buttons(True)
    
    def load_file(self):
        if self._handler_is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
        loaded_file_name = filedialog.askopenfilename(title="Select a file")
        if not loaded_file_name:
            return
        if not self._handler_import_image(loaded_file_name):
            messagebox.showerror(title="Operation cancelled", message="Failed to load image")
            return
        self._gui_clear_selection()
        self._gui_refresh_image()
        self._gui_refresh_history()
        self._gui_refresh_zoom()
        self.toggle_buttons(True)
        
    def save_file(self):
        if self._handler_is_active_image() is not None:
            # get the saved file path, if any
            file_path: str = self._handler_get_file_path()
            # initialize the list of available file types
            file_types = [("PNG", "*.png"), ("JPEG", "*.jpg")]
            
            if file_path is None:
                # no loaded image; use default values
                file_path = ""
                file_name = "image"
                file_type = "png"
                file_dir = file_path
            else:
                # determine values from the loaded image's saved info
                file_name = file_path.split("/")[-1]
                # determine the filetype name, eg "JPEG"
                file_type = file_name.split(".")[-1].upper()
                if file_type == "JPG":
                    file_type = "JPEG"
                # move the loaded filetype to the front of the file_types list
                for i in range(len(file_types)):
                    if file_types[i][0] == file_type:
                        file_types.insert(0, file_types.pop(i))
                        break
                file_dir = file_path[len(file_name):]
            
            path = filedialog.asksaveasfilename(title="Save as:", initialdir=file_dir, initialfile=file_name, defaultextension=file_type, filetypes=file_types)
            if path is not None and path != "":
                success = self._handler_export_image(path)
                if success:
                    messagebox.showinfo("Save Success", "File saved successfully.")
                else:
                    messagebox.showerror("Save Error", "Error saving image.")
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
        dimension_dialog = CanvasDialog(self._root, title="Resize Image", color_codes=self._gui_get_color_codes(), use_color=False)
        if dimension_dialog.width is None or dimension_dialog.height is None:
            return
        width = dimension_dialog.width
        height = dimension_dialog.height
        
        if width < 1 or width >= GUI_Defaults.IMAGE_MAX_WIDTH.value or height < 1 or height >= GUI_Defaults.IMAGE_MAX_HEIGHT.value:
            messagebox.showerror(title="Operation cancelled", message=f"Invalid value: Dimensions must be from 1x1 to {GUI_Defaults.IMAGE_MAX_WIDTH.value}x{GUI_Defaults.IMAGE_MAX_HEIGHT.value}")
            return
        
        self._gui_clear_selection()
        self._handler_resize((dimension_dialog.width, dimension_dialog.height))
        self._gui_refresh_history()
        self._gui_refresh_image()
        
    def toggle_buttons(self, toggle_on: bool):
        """Enable buttons which are only usable when an image is loaded;
        Also used for disabling them upon initialization"""
        state = "active" if toggle_on else "disabled"
        
        filemenu: tk.Menu = self.menu_storage[self.menubar]["File"][0]
        # toggle Save As command
        filemenu.entryconfig(2, {"state": state})
        
        editmenu: tk.Menu = self.menu_storage[self.menubar]["Edit"][0]
        # toggle Filters menu
        editmenu.entryconfig(0, {"state": state})
        # toggle Resize command
        editmenu.entryconfig(1, {"state": state})
        
        self._gui_toggle_buttons(toggle_on)
        
    def toggle_resize(self, toggle_on: bool):
        state = "active" if toggle_on else "disabled"
        editmenu: tk.Menu = self.menu_storage[self.menubar]["Edit"][0]
        editmenu.entryconfig(1, {"state": state})

    def display_keybinds(self):
        msg = f""
        for item in GUI_Defaults:
            if "KEYBIND" in item.name:
                msg += f"{item.name[8:]}: {item.value[1:-1]}\n"
        msg = msg[:-1] # chop off trailing newline
        self.display_help_message("Keybinds", msg)
        
    def display_about_message(self):
        title = f"SIMPLE v{GUI_Defaults.VERSION.value}"
        msg = """SIMPLE: Simple IMage Processor for Lazy Editors
        
        Contributors:
        \tAddison Casner
        \tDerek Jennings
        \tQuinn Pulley
        \tWill Verplaetse"""
        self.display_help_message(title, msg)
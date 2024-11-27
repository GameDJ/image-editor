import os
import tkinter as tk
from tkinter import Menu, ttk, simpledialog, filedialog, commondialog, dialog, colorchooser, font, messagebox
import PIL.Image
import numpy as np
import PIL
from PIL import ImageTk
from FilterType import FilterType, FilterInfo
from RequestHandler import RequestHandler
from ArgumentType import ArgumentType
from Arguments import Arguments
from ShapeType import ShapeType
from Image_GUI import Image_GUI
from ImageMode import ImageMode
from History_GUI import History_GUI
from Selection_GUI import Selection_GUI
from Color_GUI import Color_GUI
from Image import Image
from CanvasDialog_GUI import CanvasDialog
from Draw_GUI import Draw_GUI
from Zoom_GUI import Zoom_GUI
from GUI_Defaults import GUI_Defaults

def printy(text, *args):
    print("printy", text, *args)
    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("SIMPLE")
    window.geometry('800x560')
    
    PANEL_TITLE_FONT = font.Font(size=12, underline=False, slant="italic")
    
    # for storing bindings under a unique key
    bindings = {}
    
    handler = RequestHandler()
    
    # image mode refers to when and for what purpose the image preview is clickable
    current_image_mode = ImageMode.NONE
    def change_image_mode(new_mode: ImageMode):
        """Change the image mode and reset the visual state of the button previously in use, if any"""
        global current_image_mode
        # print("current image mode:", current_image_mode)
        # Turn off current mode
        if current_image_mode == ImageMode.SELECT:
            selection_gui.toggle_select_off()
        elif current_image_mode == ImageMode.EYEDROP:
            color_gui.toggle_eyedropper_off()
        elif current_image_mode == ImageMode.SHAPE:
            draw_gui.toggle_drawing_off()
        if current_image_mode == new_mode:
            # if the same mode was selected, toggle it off
            # (the other toggle off functions were handled above)
            current_image_mode = ImageMode.NONE
        else:
            # Turn on new mode
            current_image_mode = new_mode
            if new_mode == ImageMode.SELECT:
                selection_gui.toggle_select_on()
            elif new_mode == ImageMode.EYEDROP:
                color_gui.toggle_eyedropper_on()
            elif new_mode == ImageMode.SHAPE:
                draw_gui.toggle_drawing_on()
        # print("new image mode:", current_image_mode)
        
        # Set cursor based on action
        if current_image_mode == ImageMode.NONE:
            image_gui.set_cursor(GUI_Defaults.CURSOR.value)
        else:
            image_gui.set_cursor(GUI_Defaults.CURSOR_IMG_ACTION.value)
            
    
    ### MENU BAR ###
    menubar = tk.Menu(window, title="Menubar")
        
    def create_canvas():
        if handler.is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
            
        canvasDialog = CanvasDialog(window, title="Initialize Canvas", color_codes=color_gui.color_codes)
        if not canvasDialog.width or not canvasDialog.height:
            messagebox.showerror(title="Operation cancelled", message="Failed to create canvas")
        else:
            handler.create_canvas(canvasDialog.width, canvasDialog.height, canvasDialog.color_codes[0])
            image_gui.refresh_image()
            # activate_savebtn()
            history_gui.refresh_history()
    
    def load_file():
        if handler.is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
        global loaded_file_name
        loaded_file_name = filedialog.askopenfilename(title="Select a file")
        if not loaded_file_name:
            messagebox.showerror(title="Operation cancelled", message="No file selected")
            return
        if not handler.import_image(loaded_file_name):
            messagebox.showerror(title="Operation cancelled", message="Failed to load image")
            return
        image_gui.refresh_image()
        # activate_savebtn()
        history_gui.refresh_history()
        
    def save_file():
        if handler.is_active_image() is not None:
            path = filedialog.asksaveasfilename(title="Save as:", initialfile=loaded_file_name, defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            handler.export_image(path)
            # should check to see if the file exists now, to verify it saved
        else:
            messagebox.showerror(title="Error", message="No image loaded")
        
    def filter_action(filter):
        args = Arguments()
        args.add_filter(filter)
        for arg in FilterInfo[filter]["args"]:
            if arg == ArgumentType.AMOUNT:
                args.add_amount(simpledialog.askfloat(title="Amount entry", prompt="Enter amount:"))
            elif arg == ArgumentType.COLOR:
                args.add_color(colorchooser.askcolor(title="Choose a color")[1])
        # handler will add image and selection to args before passing it to the edit class
        handler.edit(args)
        history_gui.refresh_history()
        image_gui.refresh_image()
    
    def help_message(title: str, text: str):
        messagebox.showinfo(title=title, message=text)
    
    # HELP MENU
    # more legible version for slightly(?) more computational cost
    menu_structure = {
        "File": {
            "Create blank canvas": lambda: create_canvas(),
            "Load": lambda: load_file(),
            "Save as": lambda: save_file()
        },
        "Edit": { 
            # populate the edit commands based on available filters
            FilterInfo[filter]["text"]:lambda filter=filter: filter_action(filter) for filter in FilterInfo 
        },
        "Help": {
            "Usage": {
                "File menu": {
                    "Create blank canvas": lambda: help_message("Create blank canvas", "placeholder"),
                    "Load image": lambda: help_message("Load image", "placeholder"),
                    "Save as": lambda: help_message("Save as", "placeholder"),
                }
            },
            "About": lambda: help_message("SIMPLE v1.0.0", "SIMPLE: Simple IMage Processor for Lazy Editors\n\nContributors:\n\tAddison Casner\n\tDerek Jennings\n\tQuinn Pulley\n\tWill Verplaetse")
        }
    }
    
    # def activate_savebtn():
    #     if menu_structure["File"]["Save as"].entrycget("Save as", "state") != "active":
    #         menu_structure["File"]["Save as"].entryconfig("Save as", state="active")
            
    def generate_menu(parent_menu: Menu, parent_obj: dict, cur_key: str, cur_level_obj):
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
                generate_menu(new_submenu, parent_obj[new_submenu], next_level_key, cur_level_obj[next_level_key])
        else:
            # add a command
            parent_menu.add_command(label=cur_key, command=cur_level_obj)
    # we'll use this to keep track of menus as we generate them
    menu_storage = {menubar: {}}
    for submenu in menu_structure:
        generate_menu(menubar, menu_storage[menubar], submenu, menu_structure[submenu])
    
    ### IMAGE PREVIEW ###
    image_gui = Image_GUI(
        window,
        handler.get_render_image,
    )
    # this one is packed within the class constructor
    
    #### RIGHTSIDE FRAME ####
    rightside_frame = tk.Frame(window, highlightthickness=1, highlightbackground="black")
    rightside_frame.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")
    
    ## HISTORY MENU ##
    history_gui = History_GUI(
        rightside_frame,
        PANEL_TITLE_FONT,
        handler.history_undo, 
        handler.history_redo,
        handler.history_get_index,
        handler.history_set_index,
        handler.history_descriptions,
        image_gui.refresh_image
    )
    history_gui.frame.grid(row=0, rowspan=2, padx=1, pady=1)
    
    # key bindings
    bindings[GUI_Defaults.KEYBIND_UNDO] = window.bind(GUI_Defaults.KEYBIND_UNDO.value, history_gui.undo)
    bindings[GUI_Defaults.KEYBIND_REDO] = window.bind(GUI_Defaults.KEYBIND_REDO.value, history_gui.redo)
    bindings[GUI_Defaults.KEYBIND_REDO2] = window.bind(GUI_Defaults.KEYBIND_REDO2.value, history_gui.redo)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(cnf=GUI_Defaults.SEPARATOR_CNF.value, row=2)
    
    ## SELECTION MENU ##
    # selection_frame = tk.Frame(rightside_frame)
    selection_gui = Selection_GUI(
        rightside_frame,
        PANEL_TITLE_FONT,
        image_gui.change_image_mode,
        handler.make_selection,
        handler.get_selection_bbox,
        handler.clear_selection,
        handler.get_image_dimensions,
        bindings,
        image_gui.image_preview,
        image_gui.refresh_image
    )
    selection_gui.frame.grid(row=3, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    # key bindings
    bindings[GUI_Defaults.KEYBIND_SELECT] = window.bind(GUI_Defaults.KEYBIND_SELECT.value, lambda _: change_image_mode(ImageMode.SELECT))
    bindings[GUI_Defaults.KEYBIND_CLEAR_SELECTION] = window.bind(GUI_Defaults.KEYBIND_CLEAR_SELECTION.value, selection_gui.clear_selection)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(cnf=GUI_Defaults.SEPARATOR_CNF.value, row=6)
    
    ## COLOR ##
    color_gui = Color_GUI(
        rightside_frame,
        PANEL_TITLE_FONT,
        image_gui.change_image_mode,
        handler.get_color_at_pixel,
        bindings,
        image_gui.image_preview,
        image_gui.refresh_image
    )
    color_gui.frame.grid(row=7, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")

    bindings[GUI_Defaults.KEYBIND_EYEDROPPER] = window.bind(GUI_Defaults.KEYBIND_EYEDROPPER.value, lambda _: change_image_mode(ImageMode.EYEDROP))
    
    
    ## DRAW MENU ##
    draw_gui = Draw_GUI(
        rightside_frame,
        PANEL_TITLE_FONT,
        image_gui.change_image_mode,
        handler.edit,
        handler.get_image_dimensions,
        color_gui.get_color_codes,
        bindings,
        image_gui.image_preview,
        image_gui.refresh_image,
        history_gui.refresh_history
    )
    draw_gui.frame.grid(row=9, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    bindings[GUI_Defaults.KEYBIND_DRAW] = window.bind(GUI_Defaults.KEYBIND_DRAW.value, lambda _: change_image_mode(ImageMode.SHAPE))
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(cnf=GUI_Defaults.SEPARATOR_CNF.value, row=12)
    
    ## ZOOM MENU ##
    zoom_gui = Zoom_GUI(
        rightside_frame,
        PANEL_TITLE_FONT,
        handler.zoom_change,
        image_gui.refresh_image
    )
    zoom_gui.frame.grid(row=13, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    bindings[GUI_Defaults.KEYBIND_ZOOM_IN] = window.bind(GUI_Defaults.KEYBIND_ZOOM_IN.value, lambda _: zoom_gui.zoom_change(1))
    bindings[GUI_Defaults.KEYBIND_ZOOM_OUT] = window.bind(GUI_Defaults.KEYBIND_ZOOM_OUT.value, lambda _: zoom_gui.zoom_change(-1))

    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(cnf=GUI_Defaults.SEPARATOR_CNF.value, row=15)
    
    
    window.config(menu=menubar)
    
    window.mainloop()
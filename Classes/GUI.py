import os
import tkinter as tk
from tkinter import Menu, ttk, simpledialog, filedialog, commondialog, dialog, colorchooser, font, messagebox
import numpy as np
from PIL import Image, ImageTk
from FilterType import FilterType, FilterInfo
from RequestHandler import RequestHandler
from ArgumentType import ArgumentType
from Arguments import Arguments
from History_GUI import History_GUI

from enum import Enum, auto
class ImageMode(Enum):
    NONE = auto()
    SELECT = auto()
    EYEDROP = auto()
    SHAPE = auto()

def printy(text, *args):
    print("printy", text, *args)
    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Helo vorld")
    window.geometry('800x560')
    
    class Defaults(Enum):
        BUTTON_RELIEF = "raised"
        BUTTON_TOGGLED_RELIEF = "solid"
        FONT = font.Font(size=12, underline=False, slant="italic")
        SEPARATOR_CNF = {"column":0, "columnspan":1, "rowspan":1, "sticky":"nsew"}
    
    # for storing bindings under a unique key
    bindings = {}
    
    handler = RequestHandler()
    
    # image mode refers to when and for what purpose the image preview is clickable
    current_image_mode = ImageMode.NONE
    def change_image_mode(new_mode: ImageMode):
        """Change the image mode and reset the visual state of the button previously in use, if any"""
        global current_image_mode
        print("current image mode:", current_image_mode)
        if current_image_mode == ImageMode.SELECT:
            toggle_select_off()
        elif current_image_mode == ImageMode.EYEDROP:
            toggle_eyedropper_off()
        elif current_image_mode == ImageMode.SHAPE:
            toggle_drawing_off()
        if current_image_mode == new_mode:
            # if the same mode was selected, toggle it off
            # (the other toggle off functions were handled above)
            current_image_mode = ImageMode.NONE
        else:
            # set new mode
            current_image_mode = new_mode
            if new_mode == ImageMode.SELECT:
                toggle_select_on()
            elif new_mode == ImageMode.EYEDROP:
                toggle_eyedropper_on()
            elif new_mode == ImageMode.SHAPE:
                toggle_drawing_on()
        print("new image mode:", current_image_mode)
            
    
    ### MENU BAR ###
    menubar = tk.Menu(window, title="Menubar")
        
    def create_canvas():
        if handler.is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
        
        width = simpledialog.askinteger("Canvas width", "Enter width:")
        if not width:
            messagebox.showerror(title="Operation cancelled", message="Failed to create canvas")
            return
        height = simpledialog.askinteger("Canvas height", "Enter height:")
        if not height:
            messagebox.showerror(title="Operation cancelled", message="Failed to create canvas")
            return
        color = colorchooser.askcolor(title="Choose a color")
        if not color:
            messagebox.showerror(title="Operation cancelled", message="Failed to create canvas")
            return
        
        the_image_array = np.full((height, width, 3), color[0], dtype=np.uint8)
        handler.initialize_image(the_image_array)
        refresh_image()
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
            messagebox.showerror(title="Operation cancelled", message="Failed to load image")
            return
        loaded_file_name = loaded_file_name.split("/")[-1]
        image = Image.open(loaded_file_name).convert('RGB')
        if not image:
            messagebox.showerror(title="Operation cancelled", message="Failed to load image")
            return
        the_image_array = np.array(image)
        handler.initialize_image(the_image_array)
        refresh_image()
        # activate_savebtn()
        history_gui.refresh_history()
        
    def save_file():
        if handler.is_active_image() is not None:
            path = filedialog.asksaveasfilename(title="Save as:", initialfile=loaded_file_name, defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            image = Image.fromarray(handler.get_current_actual_image())
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(path)
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
            elif arg == ArgumentType.SHAPE:
                args.add_shape(selected_shape)
        # handler will add image and selection to args before passing it to the edit class
        handler.edit(args)
        history_gui.refresh_history()
        refresh_image()
    
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
    image_frame = tk.Frame(window, width=400, height=300, background="#000000", borderwidth=1)
    # image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    image_frame.grid(row=0, column=0, rowspan=3, columnspan=3, padx=3, pady=3, sticky="nsew")
    window.grid_rowconfigure(0, minsize=300, weight=1)
    window.grid_columnconfigure(0, minsize=400, weight=1)
    
    # a label to hold the image
    img_preview = tk.Label(image_frame, borderwidth=0, cursor="circle")
    # img_preview.pack(side=tk.TOP)
    # img_preview.grid(sticky="nsew")
    img_preview.place(in_=image_frame, anchor="c", relx=.5, rely=.5)
    
    loaded_file_name = "image.png"
    
    def refresh_image():
        """Regenerate the image preview from the render image provided by RequestHandler"""
        new_image = Image.fromarray(handler.get_render_image_array())
        new_tk_image = ImageTk.PhotoImage(new_image)
        # update the image label
        img_preview.config(image=new_tk_image)
        # prevent garbage collector from deleting image?
        img_preview.image = new_tk_image

    
    #### RIGHTSIDE FRAME ####
    rightside_frame = tk.Frame(window, highlightthickness=1, highlightbackground="black")
    rightside_frame.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")
    
    ## HISTORY MENU ##
    history_gui = History_GUI(
        rightside_frame, 
        Defaults.FONT, 
        handler.history_undo, 
        handler.history_redo,
        handler.history_get_index,
        handler.history_set_index,
        handler.history_descriptions,
        refresh_image
    )
    history_gui.frame.grid(row=0, rowspan=2, padx=1, pady=1)
    
    bindings["<Control-z>"] = window.bind("<Control-z>", history_gui.undo)
    bindings["<Control-y>"] = window.bind("<Control-y>", history_gui.redo)
    bindings["<Control-Shift-Z>"] = window.bind("<Control-Shift-Z>", history_gui.redo)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(cnf=Defaults.SEPARATOR_CNF.value, row=2)
    
    ## SELECTION MENU ##
    selection_frame = tk.Frame(rightside_frame)
    selection_frame.grid(row=3, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    label = tk.Label(selection_frame, text="Select", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side=tk.TOP)
    
    selection_btn_frame = tk.Frame(selection_frame)
    selection_btn_frame.pack(side=tk.TOP)
    
    # gonna replace this with a check in handler for if selection exists
    clear_sel_state = "disabled"
        
    def toggle_select_on():
        selection_button.config(relief=Defaults.BUTTON_TOGGLED_RELIEF.value)
        global clear_sel_state
        clear_sel_state = "active"
    def toggle_select_off():
        selection_button.config(relief=Defaults.BUTTON_RELIEF.value)
        clear_sel_btn.config(state=clear_sel_state)
    
    selection_button = tk.Button(selection_btn_frame, text="Select", command=lambda:change_image_mode(ImageMode.SELECT))
    selection_button.pack(side=tk.LEFT)
    
    # clear selection button
    def clear_selection():
        global clear_sel_state
        sel_coord_1.config(text="No selection")
        sel_coord_2.config(text="")
        clear_sel_state = "disabled"
        clear_sel_btn.config(state=clear_sel_state)
    
    clear_sel_btn = tk.Button(selection_btn_frame, text="Clear", command=clear_selection, state="disabled")
    clear_sel_btn.pack(side=tk.LEFT)
    
    # coordinate display
    sel_coord_1 = tk.Label(selection_frame, text="No selection")
    sel_coord_1.pack()
    sel_coord_2 = tk.Label(selection_frame, text="")
    sel_coord_2.pack()
    
    # def fake_select():
    #     sel_coord_1.config(text="x: 20, 40")
    #     sel_coord_2.config(text="y: 30, 50")
    
    # fake_select_btn = tk.Button(selection_frame, text="Selection Tool", command=fake_select)
    # fake_select_btn.pack(side=tk.TOP)
    
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    # separator.grid(row=6, column=0, columnspan=1, rowspan=1, sticky="nsew")
    separator.grid(cnf=Defaults.SEPARATOR_CNF.value, row=6)
    
    ## DRAW MENU ##
    # draw_menu_frame = tk.Frame(rightside_frame, highlightthickness=1, highlightbackground="blue")
    draw_menu_frame = tk.Frame(rightside_frame)
    draw_menu_frame.grid(row=7, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    label = tk.Label(draw_menu_frame, text="Draw", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side = tk.TOP)
    
    draw_inner_frame = tk.Frame(draw_menu_frame)
    draw_inner_frame.pack(side = tk.TOP)
    
    def toggle_drawing_on():
        draw_btn.config(relief=Defaults.BUTTON_TOGGLED_RELIEF.value)
    def toggle_drawing_off():
        draw_btn.config(relief=Defaults.BUTTON_RELIEF.value)
            
    draw_btn = tk.Button(draw_inner_frame, text="Draw", command=lambda:change_image_mode(ImageMode.SHAPE))
    draw_btn.pack(side=tk.LEFT)
    
    options_list = ["Pen", "Rectangle"]
    selected_shape = tk.StringVar(draw_inner_frame)
    selected_shape.set(options_list[0])
    draw_optionmenu = tk.OptionMenu(draw_inner_frame, selected_shape, *options_list)
    draw_optionmenu.pack(side=tk.LEFT)
    
    ##
    # separator = ttk.Separator(rightside_frame, orient="horizontal")
    # separator.grid(row=9, column=0, columnspan=1, rowspan=1, sticky="nsew")
    
    ## COLOR ##
    # color_menu_frame = tk.Frame(rightside_frame, highlightthickness=1, highlightbackground="red")
    color_menu_frame = tk.Frame(rightside_frame)
    color_menu_frame.grid(row=10, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    label = tk.Label(color_menu_frame, text="Color", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side = tk.TOP)
    
    def convert_color_to_hex(rgb: np.ndarray):
        return "#%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])
    
    cur_color = (255, 0, 0)
    
    def change_color():
        global cur_color
        color = colorchooser.askcolor(title="Choose color", initialcolor=convert_color_to_hex(cur_color))
        if all(color):
            print(color)
            cur_color = color[0]
            update_color()
    
    def update_color():
        color_preview.config(background=convert_color_to_hex(cur_color))
    
    color_inner_frame = tk.Frame(color_menu_frame)
    color_inner_frame.pack(side=tk.TOP)
    
    fakeimage = tk.PhotoImage(width=1, height=1)
    color_preview = tk.Button(color_inner_frame, text="", image=fakeimage, width=24, height=24, compound="c", command=change_color, background=convert_color_to_hex(cur_color), relief="groove")
    color_preview.grid(row=0, column=1, padx=3)
    update_color()
    
    # eyedropper
    
    def select_pixel_color(event):
        global cur_color
        cur_color = handler.get_color_at_pixel(event.x, event.y)
        update_color()
            
    def toggle_eyedropper_on():
        bindings["select_pixel_color"] = img_preview.bind("<ButtonPress-1>", select_pixel_color)
        eyedropper_btn.config(relief=Defaults.BUTTON_TOGGLED_RELIEF.value)
    def toggle_eyedropper_off():
        img_preview.unbind("<begin_selection-1>", bindings["select_pixel_color"])
        bindings.pop("select_pixel_color")
        eyedropper_btn.config(relief=Defaults.BUTTON_RELIEF.value)
    
    # eyedropper_btn = tk.Button(color_menu_frame, text="Eyedropper", command=toggle_eyedropper, relief=Defaults.BUTTON_RELIEF.value)
    # eyedrop_img = tk.PhotoImage(file=r"C:\\Users\\derek\\OneDrive\\Documents\\2024_Fall\\IT326\\icons8-color-dropper-24.png")
    eyedrop_img = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), r"..\assets\icons8-color-dropper-24.png"))
    eyedropper_btn = tk.Button(color_inner_frame, command=lambda:change_image_mode(ImageMode.EYEDROP), relief=Defaults.BUTTON_RELIEF.value, image=eyedrop_img)
    # eyedropper_btn.pack(side=tk.TOP)
    eyedropper_btn.grid(row=0, column=3, padx=3)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    # separator.grid(row=12, column=0, columnspan=1, rowspan=1, sticky="nsew")
    separator.grid(cnf=Defaults.SEPARATOR_CNF.value, row=12)
    
    ## ZOOM MENU ##
    zoom_frame = tk.Frame(rightside_frame)
    zoom_frame.grid(row=13, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    label = tk.Label(zoom_frame, text="Zoom", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side = tk.TOP)
    
    zoom_inner_frame = tk.Frame(zoom_frame)
    zoom_inner_frame.pack(side=tk.TOP)
    
    zoom_level = 1.0
    
    def zoom_change(delta: int):
        zoom_level = handler.zoom_change(delta)
        if zoom_level < 0:
            zoom_level_label.config(text=f"1/{2**(int(zoom_level)*-1)}x")
        else:
            zoom_level_label.config(text=f"{int(zoom_level)}x")
        
    
    zoom_out_btn = tk.Button(zoom_inner_frame, text="-", command=lambda: zoom_change(-1), image=fakeimage, compound="c", width=20, height=20)
    zoom_out_btn.pack(side=tk.LEFT, padx=1)
    
    zoom_level_label = tk.Label(zoom_inner_frame, text=f"1x")
    zoom_level_label.pack(side=tk.LEFT, padx=3)
    
    zoom_in_btn = tk.Button(zoom_inner_frame, text="+", command=lambda: zoom_change(1), image=fakeimage, compound="c", width=20, height=20)
    zoom_in_btn.pack(side=tk.LEFT, padx=1)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    # separator.grid(row=15, column=0, columnspan=1, rowspan=1, sticky="nsew")
    separator.grid(cnf=Defaults.SEPARATOR_CNF.value, row=15)
    
    
    window.config(menu=menubar)
    
    window.mainloop()
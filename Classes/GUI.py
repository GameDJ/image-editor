import os
import tkinter as tk
from tkinter import Menu, ttk, simpledialog, filedialog, commondialog, dialog, colorchooser, font, messagebox
import numpy as np
from PIL import Image, ImageTk
from FilterType import FilterType, FilterInfo
from RequestHandler import RequestHandler
from ArgumentType import ArgumentType
from Arguments import Arguments

def printy(text, *args):
    print("printy", text, *args)
    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Helo vorld")
    window.geometry('800x560')
    
    bindings = {}
    
    handler = RequestHandler()
    
    ### MENU BAR ###
    menubar = tk.Menu(window, title="Menubar")
    
    # index of NEXT history item
    hist_len = 0
        
    def create_canvas():
        if handler.is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
        global the_image_array, hist_len
        
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
        # hist_len +=1
        # history_listbox.insert(hist_len, "Create canvas")
        # history_ui_add_item("Create canvas")
        refresh_history()
    
    def load_file():
        if handler.is_active_image():
            discard_image = messagebox.askyesno(message="Are you sure you want to discard the current image?")
            if not discard_image: 
                return
        global loaded_file_name, the_image_array, hist_len
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
        # hist_len +=1
        # history_listbox.insert(hist_len, "Load file")
        # history_ui_add_item("Load file")
        refresh_history()
        
    def save_file():
        if handler.is_active_image() is not None:
            path = filedialog.asksaveasfilename(title="Save as:", initialfile=loaded_file_name, defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            image = Image.fromarray(the_image_array)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(path)
            # should check to see if the file exists now, to verify it saved
        else:
            messagebox.showerror(title="Error", message="No image loaded")
    
    # FILE MENU
    # filemenu = tk.Menu(menubar, tearoff=0)
    # filemenu.add_command(label="Create blank canvas", command=lambda: create_canvas())
    # filemenu.add_command(label="Load", command=lambda: load_file())
    # filemenu.add_command(label="Save as", command=lambda: save_file(), state="disabled")
    # menubar.add_cascade(label="File", menu=filemenu)
    
    # EDIT MENU
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
        # update the history list on the ui
        # history_ui_add_item(FilterInfo[filter]["text"])
        refresh_history()
        refresh_image()
        
    # editmenu = tk.Menu(menubar, tearoff=0)
    # for filter in FilterInfo:
    #     editmenu.add_command(label=FilterInfo[filter]["text"], command=lambda filter=filter: filter_action(filter))
    # menubar.add_cascade(label="Edit", menu=editmenu)
    
    # HISTORY MENU
    # historymenu = tk.Menu(menubar, tearoff=0)
    # historymenu.add_command(label="Undo", command=lambda: printy("undo"))
    # historymenu.add_command(label="Redo", command=lambda: printy("redo"))
    # menubar.add_cascade(label="History", menu=historymenu)
    
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
    # direct version
    # helpmenu = tk.Menu(menubar, tearoff=0)
    # menubar.add_cascade(label="Help", menu=helpmenu)
    # usage_helpmenu = tk.Menu(helpmenu, tearoff=0)
    # helpmenu.add_cascade(label="Usage", menu=usage_helpmenu)
    # file_usage_helpmenu = tk.Menu(usage_helpmenu, tearoff=0)
    # usage_helpmenu.add_cascade(label="File menu", menu=file_usage_helpmenu)
    # file_usage_helpmenu.add_command(label="Create blank canvas", command=lambda: help_message("Create blank canvas", "placeholder"))
    # file_usage_helpmenu.add_command(label="Load image", command=lambda: help_message("Load image", "placeholder"))
    # file_usage_helpmenu.add_command(label="Save as", command=lambda: help_message("Save as", "placeholder"))
    # helpmenu.add_command(label="About", command=lambda: help_message("SIMPLE v1.0.0", "SIMPLE: Simple IMage Processor for Lazy Editors\n\nContributors:\n\tAddison Casner\n\tDerek Jennings\n\tQuinn Pulley\n\tWill Verplaetse"))

    
    
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
    the_image_array: np.ndarray = np.empty((0,0))
    
    def update_img_preview():
        new_image = Image.fromarray(the_image_array)
        new_tk_image = ImageTk.PhotoImage(new_image)
        # update the image label
        img_preview.config(image=new_tk_image)
        # prevent garbage collector from deleting image?
        img_preview.image = new_tk_image
    
    #### RIGHTSIDE FRAME ####
    rightside_frame = tk.Frame(window, highlightthickness=1, highlightbackground="black")
    rightside_frame.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")
    
    ## HISTORY MENU ##
    # history_frame = tk.Frame(rightside_frame, highlightthickness=1, highlightbackground="brown")
    history_frame = tk.Frame(rightside_frame)
    history_frame.grid(row=0, rowspan=2, padx=1, pady=1)
    
    label = tk.Label(history_frame, text="History", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side = tk.TOP)
    
    history_btn_frame = tk.Frame(history_frame)
    history_btn_frame.pack(side=tk.TOP)
    def history_ui_remove_item():
        history_listbox.delete(tk.END)
        history_listbox.activate(tk.END)
        history_listbox.focus()
    def history_ui_add_item(desc: str):
        history_listbox.insert(tk.END, desc)
        history_listbox.activate(tk.END)
        history_listbox.focus()
        
    def refresh_history():
        history_listbox.delete(0, tk.END)
        entry_descs = handler.history_descriptions()
        for entry_desc in entry_descs:
            history_listbox.insert(tk.END, entry_desc[1])
        history_listbox.activate(handler.get_history_index())
        history_listbox.focus()
        if handler.get_history_index() <= 0:
            # first entry is selected; no more undo
            undo_btn.config(state="disabled")
        else:
            undo_btn.config(state="active")
        if handler.get_history_index() >= len(entry_descs)-1:
            # latest entry is selected; can't redo
            redo_btn.config(state="disabled")
        else:
            redo_btn.config(state="active")
            
    def refresh_image():
        global the_image_array
        the_image_array = handler.get_current_image()
        update_img_preview()
    
    def history_undo():
        # update data
        handler.history_undo()
        ## update ui: image preview and history listbox
        refresh_image()
        refresh_history()
    def history_redo():
        handler.history_redo()
        refresh_image()
        refresh_history()
    undo_btn = tk.Button(history_btn_frame, text="Undo", command=lambda: history_undo(), state="disabled")
    undo_btn.grid(column=0, row=0)
    redo_btn = tk.Button(history_btn_frame, text="Redo", command=lambda: history_redo(), state="disabled")
    redo_btn.grid(column=1, row=0)
    
    history_listbox = tk.Listbox(history_frame)
    history_listbox.pack(padx=1, pady=1)
    def onselct(event):
        print(event)
    history_listbox.bind("<<ListboxSelect>>", onselct)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(row=2, column=0, columnspan=1, rowspan=1, sticky="nsew")
    
    ## SELECTION MENU ##
    # selection_frame = tk.Frame(rightside_frame, highlightthickness=1, highlightbackground="green")
    selection_frame = tk.Frame(rightside_frame)
    selection_frame.grid(row=3, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    label = tk.Label(selection_frame, text="Select", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side=tk.TOP)
    
    selection_btn_frame = tk.Frame(selection_frame)
    selection_btn_frame.pack(side=tk.TOP)
    
    selecting = False
    clear_sel_state = "disabled"
    
    def clear_sel_btn_state():
        clear_sel_btn.config(state=clear_sel_state)
        
    def toggle_select():
        global selecting, clear_sel_state
        if not selecting:
            selecting = True
            selection_button.config(relief="solid")
            clear_sel_state = "active"
        else:
            selecting = False
            selection_button.config(relief="raised")
        clear_sel_btn_state()
    
    selection_button = tk.Button(selection_btn_frame, text="Select", command=toggle_select)
    selection_button.pack(side=tk.LEFT)
    
    # clear selection button
    def clear_selection():
        global clear_sel_state
        sel_coord_1.config(text="No selection")
        sel_coord_2.config(text="")
        clear_sel_state = "disabled"
        clear_sel_btn_state()
    
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
    separator.grid(row=6, column=0, columnspan=1, rowspan=1, sticky="nsew")
    
    ## DRAW MENU ##
    # draw_menu_frame = tk.Frame(rightside_frame, highlightthickness=1, highlightbackground="blue")
    draw_menu_frame = tk.Frame(rightside_frame)
    draw_menu_frame.grid(row=7, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    label = tk.Label(draw_menu_frame, text="Draw", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side = tk.TOP)
    
    draw_inner_frame = tk.Frame(draw_menu_frame)
    draw_inner_frame.pack(side = tk.TOP)
    
    drawing = False
    
    def toggle_drawing():
        global drawing
        drawing = not drawing
        if drawing:
            draw_btn.config(relief="solid")
        else:
            draw_btn.config(relief="raised")
            
    draw_btn = tk.Button(draw_inner_frame, text="Draw", command=toggle_drawing)
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
    eyedropper_enabled = False
    
    def select_pixel_color(event):
        global the_image_array, cur_color
        cur_color = the_image_array[event.y][event.x]
        update_color()
    
    def toggle_eyedropper():
        global eyedropper_enabled
        eyedropper_enabled = not eyedropper_enabled
        if eyedropper_enabled:
            bindings["select_pixel_color"] = img_preview.bind("<ButtonPress-1>", select_pixel_color)
            eyedropper_btn.config(relief="solid")
        else:
            img_preview.unbind("<begin_selection-1>", bindings["select_pixel_color"])
            bindings.pop("select_pixel_color")
            eyedropper_btn.config(relief="raised")
    
    # eyedropper_btn = tk.Button(color_menu_frame, text="Eyedropper", command=toggle_eyedropper, relief="raised")
    # eyedrop_img = tk.PhotoImage(file=r"C:\\Users\\derek\\OneDrive\\Documents\\2024_Fall\\IT326\\icons8-color-dropper-24.png")
    eyedrop_img = tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), r"..\assets\icons8-color-dropper-24.png"))
    eyedropper_btn = tk.Button(color_inner_frame, command=toggle_eyedropper, relief="raised", image=eyedrop_img)
    # eyedropper_btn.pack(side=tk.TOP)
    eyedropper_btn.grid(row=0, column=3, padx=3)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(row=12, column=0, columnspan=1, rowspan=1, sticky="nsew")
    
    ## ZOOM MENU ##
    zoom_frame = tk.Frame(rightside_frame)
    zoom_frame.grid(row=13, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
    
    label = tk.Label(zoom_frame, text="Zoom", font=font.Font(size=12, underline=False, slant="italic"))
    label.pack(side = tk.TOP)
    
    zoom_inner_frame = tk.Frame(zoom_frame)
    zoom_inner_frame.pack(side=tk.TOP)
    
    zoom_level = 1.0
    
    def zoom_change(delta: int):
        global zoom_level
        zoom_level += delta
        if zoom_level == 0:
            zoom_level += delta
        if zoom_level < 0:
            # eg. "1/2x", "1/4x", "1/8x"
            zoom_level_label.config(text=f"1/{2**(int(zoom_level)*-1)}x")
        else:
            # eg. "1x", "2x", "3x"
            zoom_level_label.config(text=f"{int(zoom_level)}x")
    
    zoom_out_btn = tk.Button(zoom_inner_frame, text="-", command=lambda: zoom_change(-1), image=fakeimage, compound="c", width=20, height=20)
    zoom_out_btn.pack(side=tk.LEFT, padx=1)
    
    zoom_level_label = tk.Label(zoom_inner_frame, text=f"{int(zoom_level)}x")
    zoom_level_label.pack(side=tk.LEFT, padx=3)
    
    zoom_in_btn = tk.Button(zoom_inner_frame, text="+", command=lambda: zoom_change(1), image=fakeimage, compound="c", width=20, height=20)
    zoom_in_btn.pack(side=tk.LEFT, padx=1)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(row=15, column=0, columnspan=1, rowspan=1, sticky="nsew")
    
    
    window.config(menu=menubar)
    
    window.mainloop()
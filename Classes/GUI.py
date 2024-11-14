import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, commondialog, dialog, colorchooser, font
import numpy as np
from PIL import Image, ImageTk

def printy(text, *args):
    print("printy", text, *args)
    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Helo vorld")
    window.geometry('800x560')
    
    bindings = {}
    
    ## MENU BAR ##
    menubar = tk.Menu(window, title="Menubar")
    
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
        
    hist_num = 0
    
    def activate_savebtn():
        if filemenu.entrycget("Save as", "state") != "active":
            filemenu.entryconfig("Save as", state="active")
        
    def create_canvas():
        global the_image_array, hist_num
        width = simpledialog.askinteger("Canvas width", "Enter width:")
        height = simpledialog.askinteger("Canvas height", "Enter height:")
        color = colorchooser.askcolor(title="Choose color")
        the_image_array = np.full((height, width, 3), color[0], dtype=np.uint8)
        update_img_preview()
        activate_savebtn()
        hist_num +=1
        history_listbox.insert(hist_num, "Create canvas")     
    
    def load_file():
        global loaded_file_name, the_image_array, hist_num
        loaded_file_name = filedialog.askopenfilename(title="Select a file")
        loaded_file_name = loaded_file_name.split("/")[-1]
        image = Image.open(loaded_file_name).convert('RGB')
        the_image_array = np.array(image)
        update_img_preview()
        activate_savebtn()
        hist_num +=1
        history_listbox.insert(hist_num, "Load file")  
        
    def save_file():
        path = filedialog.asksaveasfilename(title="Save as:", initialfile=loaded_file_name, defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        image = Image.fromarray(the_image_array)
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(path)
    
    # FILE MENU
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Create blank canvas", command=lambda: create_canvas())
    filemenu.add_command(label="Load", command=lambda: load_file())
    filemenu.add_command(label="Save as", command=lambda: save_file(), state="disabled")
    menubar.add_cascade(label="File", menu=filemenu)
    
    # EDIT MENU
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Crop", command=lambda: print("crop"))
    editmenu.add_command(label="Flip Horizontal", command=lambda: print("flip horiz"))
    editmenu.add_command(label="Flip Vertical", command=lambda: print("flip vert"))
    editmenu.add_command(label="Invert colors", command=lambda: print("invert"))
    editmenu.add_command(label="Blur", command=lambda: print("blur"))
    menubar.add_cascade(label="Edit", menu=editmenu)
    
    # HISTORY MENU
    historymenu = tk.Menu(menubar, tearoff=0)
    historymenu.add_command(label="Undo", command=lambda: printy("undo"))
    historymenu.add_command(label="Redo", command=lambda: printy("redo"))
    menubar.add_cascade(label="History", menu=historymenu)
    
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
    undo_btn = tk.Button(history_btn_frame, text="Undo", command=lambda: printy("undo"))
    undo_btn.grid(column=0, row=0)
    redo_btn = tk.Button(history_btn_frame, text="Redo", command=lambda: printy("redo"))
    redo_btn.grid(column=1, row=0)
    
    history_listbox = tk.Listbox(history_frame)
    history_listbox.pack(padx=1, pady=1)
    
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
        sel_coord_2.config(text="No selection")
        clear_sel_state = "disabled"
        clear_sel_btn_state()
    
    clear_sel_btn = tk.Button(selection_btn_frame, text="Clear", command=clear_selection, state="disabled")
    clear_sel_btn.pack(side=tk.LEFT)
    
    # coordinate display
    sel_coord_1 = tk.Label(selection_frame, text="No selection")
    sel_coord_1.pack()
    sel_coord_2 = tk.Label(selection_frame, text="No selection")
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
    
    drawing = False
    
    def toggle_drawing():
        global drawing
        drawing = not drawing
        if drawing:
            draw_btn.config(relief="solid")
        else:
            draw_btn.config(relief="raised")
            
    draw_btn = tk.Button(draw_menu_frame, text="Draw", command=toggle_drawing)
    draw_btn.pack(side=tk.LEFT)
    
    options_list = ["Pen", "Rectangle"]
    value_inside = tk.StringVar(draw_menu_frame)
    value_inside.set(options_list[0])
    draw_optionmenu = tk.OptionMenu(draw_menu_frame, value_inside, *options_list)
    draw_optionmenu.pack(side=tk.LEFT)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(row=9, column=0, columnspan=1, rowspan=1, sticky="nsew")
    
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
    eyedrop_img = tk.PhotoImage(file=r"C:\\Users\\derek\\OneDrive\\Documents\\2024_Fall\\IT326\\icons8-color-dropper-24.png")
    eyedropper_btn = tk.Button(color_inner_frame, command=toggle_eyedropper, relief="raised", image=eyedrop_img)
    # eyedropper_btn.pack(side=tk.TOP)
    eyedropper_btn.grid(row=0, column=3, padx=3)
    
    ##
    separator = ttk.Separator(rightside_frame, orient="horizontal")
    separator.grid(row=12, column=0, columnspan=1, rowspan=1, sticky="nsew")
    
    
    window.config(menu=menubar)
    
    window.mainloop()
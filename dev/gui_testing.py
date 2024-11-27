import tkinter as tk
from tkinter import ttk

def hello_world():
    print("Hello world!")

def hello_button():
    button = ttk.Button(text="ttk Button", command=hello_world)
    button.pack()

def render_gui():
    # initialize toplevel tkinter widget
    window = tk.Tk()
    window.title("tkinter testing")
    window.geometry('200x400') 
    
    # button = ttk.Button(text="ttk Button", command=hello_world)
    # button = hello_button()
    # button.pack()
    hello_button()
    
    ######## Menu ########
    
    menubar = tk.Menu(window, title="Menubar")
    
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=hello_world)
    filemenu.add_command(label="Save", command=hello_world)
    menubar.add_cascade(label="File", menu=filemenu)
    
    filtermenu = tk.Menu(menubar, tearoff=0)
    filtermenu.add_command(label="Flip Horizontal", command=hello_world)
    filtermenu.add_command(label="Flip Vertical", command=hello_world)
    filtermenu.add_command(label="Invert colors", command=hello_world)
    filtermenu.add_command(label="Blur", command=hello_world)
    menubar.add_cascade(label="Filters", menu=filtermenu)
    
    window.config(menu=menubar)
    
    
    ######### OptionMenu ########
    
    label = tk.Label(window, text="OptionMenu:")
    label.pack( side = tk.TOP)
    # Create the list of options 
    options_list = ["Option 1", "Option 2", "Option 3", "Option 4"] 
    
    # Variable to keep track of the option 
    # selected in OptionMenu 
    value_inside = tk.StringVar(window)
    
    # Set the default value of the variable 
    value_inside.set("Select an Option")
    
    # Create the optionmenu widget and passing  
    # the options_list and value_inside to it. 
    question_menu = tk.OptionMenu(window, value_inside, *options_list) 
    question_menu.pack() 
    
    
    ####### ListBox #######
    
    label = tk.Label(window, text="ListBox:")
    label.pack( side = tk.TOP)
    list_box = tk.Listbox(window)
    list_box.insert(1, "Python")
    list_box.insert(2, "Perl")
    list_box.insert(3, "C")
    list_box.insert(4, "PHP")
    list_box.insert(5, "JSP")
    list_box.insert(6, "Ruby")

    list_box.pack()
    
    
    ####### Scale (slider) #######
    
    label = tk.Label(window, text="Scale:")
    label.pack( side = tk.TOP)
    sliderVal = tk.IntVar()
    scale = tk.Scale(window, variable=sliderVal, orient="horizontal", from_=1, to=5)
    scale.pack(anchor="center")
    
    ####### text Entry #######
    
    label = tk.Label(window, text="Entry:")
    label.pack( side = tk.TOP)
    entry = tk.Entry(window, bd =5)
    entry.pack(side = tk.TOP)
    
    # render the window
    window.mainloop()
    
    
if __name__ == "__main__":
    render_gui()

# from tkinter import *
# def donothing():
#    filewin = Toplevel(root)
#    button = Button(filewin, text="Do nothing button")
#    button.pack()

# root = Tk()
# menubar = Menu(root)
# filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", command=donothing)
# filemenu.add_command(label="Open", command=donothing)
# filemenu.add_command(label="Save", command=donothing)
# filemenu.add_command(label="Save as...", command=donothing)
# filemenu.add_command(label="Close", command=donothing)

# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=root.quit)
# menubar.add_cascade(label="File", menu=filemenu)
# editmenu = Menu(menubar, tearoff=0)
# editmenu.add_command(label="Undo", command=donothing)
# editmenu.add_separator()
# editmenu.add_command(label="Cut", command=donothing)
# editmenu.add_command(label="Copy", command=donothing)
# editmenu.add_command(label="Paste", command=donothing)
# editmenu.add_command(label="Delete", command=donothing)
# editmenu.add_command(label="Select All", command=donothing)

# menubar.add_cascade(label="Edit", menu=editmenu)
# helpmenu = Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Help Index", command=donothing)
# helpmenu.add_command(label="About...", command=donothing)
# menubar.add_cascade(label="Help", menu=helpmenu)

# root.config(menu=menubar)
# root.mainloop()
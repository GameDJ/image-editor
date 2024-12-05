from enum import Enum, auto

class GUI_Defaults(Enum):
    BUTTON_RELIEF = "raised"
    BUTTON_TOGGLED_RELIEF = "solid"
    SEPARATOR_CNF = {"column":0, "columnspan":1, "rowspan":1, "sticky":"nsew"}
    CURSOR = ""
    CURSOR_IMG_ACTION = "circle"
    CLICK_PRESS_BINDING = "<ButtonPress-1>"
    CLICK_DRAG_BINDING = "<B1-Motion>"
    CLICK_RELEASE_BINDING = "<ButtonRelease-1>"
    KEYBIND_UNDO = "<Control-z>"
    KEYBIND_REDO = "<Control-y>"
    KEYBIND_REDO2 = "<Control-Shift-Z>"
    KEYBIND_SELECT = "<s>"
    KEYBIND_CLEAR_SELECTION = "<c>"
    KEYBIND_EYEDROPPER = "<i>"
    KEYBIND_DRAW = "<d>"
    KEYBIND_ZOOM_IN = "<equal>"
    KEYBIND_ZOOM_OUT = "<minus>"
    IMAGE_MAX_WIDTH = 1600
    IMAGE_MAX_HEIGHT = 900
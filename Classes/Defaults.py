from enum import Enum, auto
from tkinter import font

class Defaults(Enum):
    BUTTON_RELIEF = "raised"
    BUTTON_TOGGLED_RELIEF = "solid"
    PANEL_TITLE_FONT = font.Font(size=12, underline=False, slant="italic")
    SEPARATOR_CNF = {"column":0, "columnspan":1, "rowspan":1, "sticky":"nsew"}
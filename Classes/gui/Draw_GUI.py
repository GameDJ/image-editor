import tkinter as tk
from tkinter import font
from typing import Callable
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
from Classes.edit.draw.ShapeType import ShapeType
from Classes.info.Selection import Selection
from Classes.gui.GUI_Defaults import GUI_Defaults

class Draw_GUI():
    def __init__(self, parent_frame: tk.Frame, gui_title_font: font, gui_change_image_mode: Callable, handler_edit: Callable, handler_get_image_dimensions: Callable, _gui_get_color_codes: Callable, gui_bindings: dict, gui_image_preview: tk.Label, gui_refresh_image: Callable, gui_refresh_history: Callable):
        # Outside refs
        self._gui_change_image_mode = gui_change_image_mode
        self._handler_edit = handler_edit
        self._handler_get_image_dimensions = handler_get_image_dimensions
        self._gui_bindings = gui_bindings
        self._gui_image_preview = gui_image_preview
        self._gui_refresh_image = gui_refresh_image
        self._gui_get_color_codes = _gui_get_color_codes
        self._gui_refresh_history = gui_refresh_history
        
        self.shape_selection = Selection()
        self._args = Arguments()
        
        # Draw panel frame
        self.frame = tk.Frame(parent_frame)
        # Label
        self.label = tk.Label(self.frame, text="Draw", font=gui_title_font)
        self.label.pack(side = tk.TOP)
        # Frame for draw button and menu
        self.inner_frame = tk.Frame(self.frame)
        self.inner_frame.pack(side=tk.TOP)
        # draw button
        self.draw_btn = tk.Button(self.inner_frame, text="Draw", command=lambda: self._gui_change_image_mode(self.toggle_drawing_on, self.toggle_drawing_off), underline=0)
        self.draw_btn.pack(side=tk.LEFT)
        
        self.options_list = [name.value for name in ShapeType]
        self.selected_shape = tk.StringVar(self.inner_frame)
        self.selected_shape.set(self.options_list[0])
        self.draw_optionmenu = tk.OptionMenu(self.inner_frame, self.selected_shape, *self.options_list)
        self.draw_optionmenu.pack(side=tk.LEFT)
        
    def toggle_drawing_on(self):
        self._gui_bindings[GUI_Defaults.CLICK_PRESS_BINDING] = self._gui_image_preview.bind(GUI_Defaults.CLICK_PRESS_BINDING.value, self._begin_shape)
        self._gui_bindings[GUI_Defaults.CLICK_DRAG_BINDING] = self._gui_image_preview.bind(GUI_Defaults.CLICK_DRAG_BINDING.value, self._making_shape)
        self._gui_bindings[GUI_Defaults.CLICK_RELEASE_BINDING] = self._gui_image_preview.bind(GUI_Defaults.CLICK_RELEASE_BINDING.value, self._released_shape)
        self.draw_btn.config(relief=GUI_Defaults.BUTTON_TOGGLED_RELIEF.value)
    
    def toggle_drawing_off(self):
        self._gui_image_preview.unbind(GUI_Defaults.CLICK_PRESS_BINDING.value, self._gui_bindings.pop(GUI_Defaults.CLICK_PRESS_BINDING))
        self._gui_image_preview.unbind(GUI_Defaults.CLICK_DRAG_BINDING.value, self._gui_bindings.pop(GUI_Defaults.CLICK_DRAG_BINDING))
        self._gui_image_preview.unbind(GUI_Defaults.CLICK_RELEASE_BINDING.value, self._gui_bindings.pop(GUI_Defaults.CLICK_RELEASE_BINDING))
        self.draw_btn.config(relief=GUI_Defaults.BUTTON_RELIEF.value)
        
    def _begin_shape(self, event: tk.Event):
        self.shape_selection.clear()
        self._args.add_shape(ShapeType(self.selected_shape.get()))
        self._args.add_color(self._gui_get_color_codes()[0])
        self.start_coord = (event.x, event.y)
    
    def _making_shape(self, event: tk.Event):
        image_dimensions = self._handler_get_image_dimensions()
        x_clamped = min(max(0, event.x), image_dimensions[1]-1)
        y_clamped = min(max(0, event.y), image_dimensions[0]-1)
        self.shape_selection.set_bbox_from_coords(self.start_coord, (x_clamped, y_clamped))
        self._args.add_selection2(self.shape_selection)
        self._gui_refresh_image(self._args)
    
    def _released_shape(self, event: tk.Event):
        # apply the shape
        if self.shape_selection.get_bbox() is not None:
            self._handler_edit(self._args)
            self._gui_refresh_image()
            self._gui_refresh_history()
    
    def toggle_buttons(self, toggle_on: bool):
        state = "active" if toggle_on else "disabled"
        self.draw_btn.config(state=state)

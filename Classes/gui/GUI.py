import tkinter as tk
from tkinter import ttk, font
from Classes.edit.filter.FilterType import FilterType, FilterInfo
from Classes.RequestHandler import RequestHandler
from Classes.info.ArgumentType import ArgumentType
from Classes.info.Arguments import Arguments
from Classes.edit.draw.ShapeType import ShapeType
from Classes.gui.Menubar_GUI import Menubar_GUI
from Classes.gui.Image_GUI import Image_GUI
from Classes.gui.ImageMode import ImageMode
from Classes.gui.History_GUI import History_GUI
from Classes.gui.Selection_GUI import Selection_GUI
from Classes.gui.Color_GUI import Color_GUI
from Classes.image.Image import Image
from Classes.gui.Draw_GUI import Draw_GUI
from Classes.gui.Zoom_GUI import Zoom_GUI
from Classes.gui.GUI_Defaults import GUI_Defaults

class GUI():
    @staticmethod
    def render():
        window = tk.Tk()
        window.title("SIMPLE")
        # window.geometry('800x560')
        # window.geometry(f'{GUI_Defaults.IMAGE_MAX_WIDTH.value + 151}x{GUI_Defaults.IMAGE_MAX_HEIGHT.value + 57}')
        window.resizable(False, False)
        
        
        PANEL_TITLE_FONT = font.Font(size=12, underline=False, slant="italic")
        
        # for storing bindings under a unique key
        bindings = {}
        
        handler = RequestHandler()

        ### IMAGE PREVIEW ###
        image_gui = Image_GUI(
            window,
            handler.get_render_image,
        )
        # this one packs its own frame into the window
        
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
        def toggle_history_keybinds(toggle_on: bool):
            if toggle_on:
                bindings[GUI_Defaults.KEYBIND_UNDO] = window.bind(GUI_Defaults.KEYBIND_UNDO.value, history_gui.undo)
                bindings[GUI_Defaults.KEYBIND_REDO] = window.bind(GUI_Defaults.KEYBIND_REDO.value, history_gui.redo)
                bindings[GUI_Defaults.KEYBIND_REDO2] = window.bind(GUI_Defaults.KEYBIND_REDO2.value, history_gui.redo)
            else:
                window.unbind(GUI_Defaults.KEYBIND_UNDO.value, bindings.pop(GUI_Defaults.KEYBIND_UNDO, None))
                window.unbind(GUI_Defaults.KEYBIND_REDO.value, bindings.pop(GUI_Defaults.KEYBIND_REDO, None))
                window.unbind(GUI_Defaults.KEYBIND_REDO2.value, bindings.pop(GUI_Defaults.KEYBIND_REDO2, None))
        
        ##
        separator = ttk.Separator(rightside_frame, orient="horizontal")
        separator.grid(cnf=GUI_Defaults.SEPARATOR_CNF.value, row=2)
        
        ## SELECTION MENU ##
        selection_gui = Selection_GUI(
            rightside_frame,
            PANEL_TITLE_FONT,
            image_gui.change_image_mode,
            handler.make_selection,
            handler.get_selection_bbox,
            handler.clear_selection,
            image_gui.get_image_preview_dimensions,
            handler.crop,
            handler.duplicate_selection,
            bindings,
            image_gui.image_preview,
            image_gui.refresh_image,
            history_gui.refresh_history
        )
        selection_gui.frame.grid(row=3, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
        
        # key bindings
        def toggle_selection_keybinds(toggle_on: bool):
            if toggle_on:
                bindings[GUI_Defaults.KEYBIND_SELECT] = window.bind(GUI_Defaults.KEYBIND_SELECT.value, lambda _: image_gui.change_image_mode(selection_gui.toggle_select_on, selection_gui.toggle_select_off))
                bindings[GUI_Defaults.KEYBIND_CLEAR_SELECTION] = window.bind(GUI_Defaults.KEYBIND_CLEAR_SELECTION.value, selection_gui.clear_selection)
            else:
                window.unbind(GUI_Defaults.KEYBIND_SELECT.value, bindings.pop(GUI_Defaults.KEYBIND_SELECT, None))
                window.unbind(GUI_Defaults.KEYBIND_CLEAR_SELECTION.value, bindings.pop(GUI_Defaults.KEYBIND_CLEAR_SELECTION, None))
        
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

        def toggle_color_keybinds(toggle_on: bool):
            if toggle_on:
                bindings[GUI_Defaults.KEYBIND_EYEDROPPER] = window.bind(GUI_Defaults.KEYBIND_EYEDROPPER.value, lambda _: image_gui.change_image_mode(color_gui.toggle_eyedropper_on, color_gui.toggle_eyedropper_off))
            else:
                window.unbind(GUI_Defaults.KEYBIND_EYEDROPPER.value, bindings.pop(GUI_Defaults.KEYBIND_EYEDROPPER, None))
        
        ## DRAW MENU ##
        draw_gui = Draw_GUI(
            rightside_frame,
            PANEL_TITLE_FONT,
            image_gui.change_image_mode,
            handler.edit,
            # handler.get_image_dimensions,
            image_gui.get_image_preview_dimensions,
            color_gui.get_color_codes,
            bindings,
            image_gui.image_preview,
            image_gui.refresh_image,
            history_gui.refresh_history
        )
        draw_gui.frame.grid(row=9, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
        
        def toggle_draw_keybinds(toggle_on: bool):
            if toggle_on:
                bindings[GUI_Defaults.KEYBIND_DRAW] = window.bind(GUI_Defaults.KEYBIND_DRAW.value, lambda _: image_gui.change_image_mode(draw_gui.toggle_drawing_on, draw_gui.toggle_drawing_off))
            else:
                window.unbind(GUI_Defaults.KEYBIND_DRAW.value, bindings.pop(GUI_Defaults.KEYBIND_DRAW, None))
        
        ##
        separator = ttk.Separator(rightside_frame, orient="horizontal")
        separator.grid(cnf=GUI_Defaults.SEPARATOR_CNF.value, row=12)
        
        def toggle_actions_while_zoomed(toggle_on: bool):
            """Disable certain edits while zoomed in/out"""
            menubar_gui.toggle_resize(toggle_on)
            image_gui.change_image_mode()
            selection_gui.toggle_buttons(toggle_on)
            toggle_selection_keybinds(toggle_on)
            selection_gui.clear_selection()
            color_gui.toggle_buttons(toggle_on)
            toggle_color_keybinds(toggle_on)
            draw_gui.toggle_buttons(toggle_on)
            toggle_draw_keybinds(toggle_on)
        
        ## ZOOM MENU ##
        zoom_gui = Zoom_GUI(
            rightside_frame,
            PANEL_TITLE_FONT,
            handler.zoom_change,
            toggle_actions_while_zoomed,
            image_gui.refresh_image
        )
        zoom_gui.frame.grid(row=13, rowspan=2, column=0, padx=1, pady=1, sticky="nsew")
        
        def toggle_zoom_keybinds(toggle_on: bool):
            if toggle_on:
                bindings[GUI_Defaults.KEYBIND_ZOOM_IN] = window.bind(GUI_Defaults.KEYBIND_ZOOM_IN.value, lambda _: zoom_gui.zoom_change(1))
                bindings[GUI_Defaults.KEYBIND_ZOOM_OUT] = window.bind(GUI_Defaults.KEYBIND_ZOOM_OUT.value, lambda _: zoom_gui.zoom_change(-1))
            else:
                window.unbind(GUI_Defaults.KEYBIND_ZOOM_IN.value, bindings.pop(GUI_Defaults.KEYBIND_ZOOM_IN, None))
                window.unbind(GUI_Defaults.KEYBIND_ZOOM_OUT.value, bindings.pop(GUI_Defaults.KEYBIND_ZOOM_OUT, None))
        
        ##
        # separator = ttk.Separator(rightside_frame, orient="horizontal")
        # separator.grid(cnf=GUI_Defaults.SEPARATOR_CNF.value, row=15)
        
        def global_toggle_buttons(toggle_on: bool):
            """Toggle buttons on/off based on whether an image is loaded"""
            toggle_history_keybinds(toggle_on)
            selection_gui.toggle_buttons(toggle_on)
            toggle_selection_keybinds(toggle_on)
            color_gui.toggle_buttons(toggle_on)
            toggle_color_keybinds(toggle_on)
            draw_gui.toggle_buttons(toggle_on)
            toggle_draw_keybinds(toggle_on)
            zoom_gui.toggle_buttons(toggle_on)
            toggle_zoom_keybinds(toggle_on)
            # menu bar handles itself; it calls this
        
        #### MENU BAR ####
        menubar_gui = Menubar_GUI(
            window,
            handler.create_canvas,
            handler.import_image,
            handler.export_image,
            handler.get_file_path,
            handler.is_active_image,
            handler.edit,
            handler.resize,
            color_gui.get_color_codes,
            history_gui.refresh_history,
            image_gui.refresh_image,
            global_toggle_buttons
        )
        
        window.config(menu=menubar_gui.menubar)
        
        window.mainloop()
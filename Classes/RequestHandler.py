from History import History
from Arguments import Arguments
from ArgumentType import ArgumentType as AT
from FilterType import FilterType, FilterInfo
from Filters import Filters
from Selection import Selection
from typing import Callable
import numpy as np

# this is a very rough framework since i have no idea what kind of information
# will be passed around here/is required for the various operations
# anyone should feel free to fill in or change stuff as needed

class RequestHandler:
    """Handles all requests."""
    
    def __init__(self):
        self.hist = History()
        self.selection = Selection()
    
    def printy(self, args: Arguments):
        print(args.get_args().keys())
    
    def initialize_image(self, image):
        self._create_history_entry(image, "Create image")
        self.zoom_level = 1
        return
    
    def export_image(self):
        return
    
    def make_selection(self, start_coord: tuple[int, int], end_coord: tuple[int, int]):
        # self.selection = Selection(start_coord, end_coord)
        self.selection.set_bbox_from_coords(start_coord, end_coord)

    def get_selection_bbox(self) -> tuple[int, int, int, int]:
        """Returns None if no bbox is set"""
        # if hasattr(self, "selection"):
        #     return self.selection
        # else:
        #     return None
        return self.selection.get_bbox()
        
    def clear_selection(self) -> bool:
        """Returns True if there was a bbox to clear, otherwise False"""
        # if hasattr(self, "selection"):
        #     del self.selection
        #     return True
        # else:
        #     return False
        return self.selection.clear()
    
    def edit(self, args: Arguments):
        args.add_image(self.hist.get_current_img())
        if self.selection.get_bbox() is not None:
            args.add_selection(self.selection)
        # self.printy(args)
        edited_image = Filters.edit(args)
        self._create_history_entry(edited_image, FilterInfo[args.get_args()[AT.FILTER]]["text"])
    
    # def _history_action(self, request):
    #     if request == "undo":
    #         self.hist.undo()
    #     elif request == "redo":
    #         self.hist.redo()
    
    def get_current_actual_image(self):
        return self.hist.get_current_img()
    
    def get_image_dimensions(self) -> tuple[int, int]:
        return self.hist.get_current_img().shape[0:2]
    
    def history_undo(self):
        self.hist.undo()
        
    def history_redo(self):
        self.hist.redo()
        
    def history_set_index(self, index: int):
        self.hist.set_index(index)
        
    def _create_history_entry(self, image_array, desc: str):
        self.hist.add_record(image_array, desc)
        
    def history_descriptions(self) -> list[tuple[int, str]]:
        return self.hist.get_entry_descriptions()
    
    def zoom_change(self, delta: int) -> int:
        self.zoom_level += delta
        if self.zoom_level == 0:
            self.zoom_level += delta        
        return self.zoom_level
        
    def get_zoom_level(self) -> int:
        if hasattr(self, self.zoom_level):
            return self.zoom_level
    
    def is_active_image(self) -> bool:
        """Returns True if history has a current image"""
        return (self.hist.get_current_img() is not None)
    
    def history_get_index(self) -> int:
        return self.hist.get_index()
    
    def get_render_image_array(self) -> np.ndarray:
        cur_img = self.hist.get_current_img()
        if self.zoom_level != 1:
            # scale based on zoom
            #
            pass
        if self.selection.get_bbox() is not None:
            # need to change the selection bounds based on zoom...
            # copy selection and scale/transform it appropriately
            #
            render_img = cur_img.copy()
            cur_img = self.selection.draw_selection(render_img)
        return cur_img
    def get_color_at_pixel(self, x: int, y: int) -> tuple[int, int, int]:
        return self.get_current_actual_image()[y][x]
    
    # def process_request(self, request):
    #     # idk how this is gonna get the information to determine which method to call so assuming string rn
    #     if request == "initialize":
    #         self._initialize_image()
    #         self._create_history_entry # save newly created image
    #     elif request == "export":
    #         self._export_image()
    #     elif request == "edit":
    #         self._edit()
    #         self._create_history_entry() # save current image version after edit
    #     elif request == "undo" or request == "redo":
    #         self._history_action(request)
    #     elif request == "color":
    #         self._get_color_information()
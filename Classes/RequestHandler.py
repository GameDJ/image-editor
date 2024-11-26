import PIL.Image
from History import History
from Arguments import Arguments
from ArgumentType import ArgumentType as AT
from FilterType import FilterType, FilterInfo
from Filters import Filters
from Selection import Selection
from Image import Image
import numpy as np
# from PIL import Image as PIL_Image
import PIL

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
    
    def create_canvas(self, width: int, height: int, color: tuple[int, int, int]):
        pass
    
    def import_image(self, file_path: str) -> bool:
        """Returns True if image initialization successful (else False)"""
        # get just the file name from the whole path
        file_name = file_path.split("/")[-1]
        # open the file as a PIL Image
        image = PIL.Image.open(file_name).convert('RGB')
        if not image:
            return False
        self.file_name = file_name
        return self.initialize_image(Image(np.array(image)))
    
    def initialize_image(self, image: Image) -> bool:
        self._create_history_entry(image, "Create image")
        self.zoom_level = 1
        return True
    
    def export_image(self):
        return
    
    def make_selection(self, start_coord: tuple[int, int], end_coord: tuple[int, int]):
        # self.selection = Selection(start_coord, end_coord)
        self.selection.set_bbox_from_coords(start_coord, end_coord)

    def get_selection_bbox(self) -> tuple[int, int, int, int]:
        """Returns None if no bbox is set"""
        return self.selection.get_bbox()
        
    def clear_selection(self) -> bool:
        """Returns True if there was a bbox to clear, otherwise False"""
        cleared = self.selection.clear()
        return cleared
    
    def edit(self, args: Arguments):
        # make a copy of the current image
        args.add_image(self.hist.get_current_img().__deepcopy__())
        # add selection, if there is one
        if self.selection.get_bbox() is not None:
            args.add_selection(self.selection)
        # edit the image
        edited_image = Filters.edit(args)
        # add the edited image to history, with the filter text as the change description
        self._create_history_entry(edited_image, FilterInfo[args.get_args()[AT.FILTER]]["text"])
    
    def get_current_actual_image(self):
        return self.hist.get_current_img()
    
    def get_image_dimensions(self) -> tuple[int, int]:
        return self.hist.get_current_img().get_img_array().shape[0:2]
    
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
    
    def get_render_image(self) -> Image:
        render_img = self.hist.get_current_img()
        if self.zoom_level != 1:
            # scale based on zoom
            #
            pass
        if self.selection.get_bbox() is not None:
            # need to change the selection bounds based on zoom...
            # copy selection and scale/transform it appropriately
            #
            render_img.set_img_array(self.selection.draw_selection(render_img.get_img_array()))
        return render_img
    
    def get_color_at_pixel(self, x: int, y: int) -> tuple[int, int, int]:
        return self.get_current_actual_image()[y][x]

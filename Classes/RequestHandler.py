from History import History
from Arguments import Arguments
from ArgumentType import ArgumentType as AT
from FilterType import FilterType, FilterInfo
from Filters import Filters
from typing import Callable

# this is a very rough framework since i have no idea what kind of information
# will be passed around here/is required for the various operations
# anyone should feel free to fill in or change stuff as needed

class RequestHandler:
    """Handles all requests."""
    
    def __init__(self):
        self.hist = History()
    
    def printy(self, args: Arguments):
        print(args.get_args().keys())
    
    def initialize_image(self, image):
        self._create_history_entry(image, "Create image")
        return
    
    def export_image(self):
        return
    
    def edit(self, args: Arguments):
        args.add_image(self.hist.get_current_img())
        # self.printy(args)
        edited_image = Filters.edit(args)
        self._create_history_entry(edited_image, FilterInfo[args.get_args()[AT.FILTER]]["text"])
    
    # def _history_action(self, request):
    #     if request == "undo":
    #         self.hist.undo()
    #     elif request == "redo":
    #         self.hist.redo()
    
    def get_current_image(self):
        return self.hist.get_current_img()
    def history_undo(self):
        self.hist.undo()
    def history_redo(self):
        self.hist.redo()
    
    def _create_history_entry(self, image_array, desc: str):
        self.hist.add_record(image_array, desc)
        
    def history_descriptions(self) -> list[tuple[int, str]]:
        return self.hist.get_entry_descriptions()
    
    def get_color_information(self):
        return
    
    def is_active_image(self) -> bool:
        """Returns True if history has a current image"""
        return (self.hist.get_current_img() is not None)
    
    def get_history_index(self) -> int:
        return self.hist.get_index()
    
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
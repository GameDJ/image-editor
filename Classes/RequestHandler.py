import History

# this is a very rough framework since i have no idea what kind of information
# will be passed around here/is required for the various operations
# anyone should feel free to fill in or change stuff as needed

class RequestHandler:
    """Handles all requests."""
    
    his = History()
    
    def _initialize_image(self):
        return
    
    def _export_image(self):
        return
    
    def _edit(self):
        return
    
    def _history_action(self, request):
        if request == "undo":
            self.his.undo()
        elif request == "redo":
            self.his.redo()
    
    def _create_history_entry(self):
        # self.his += (image_array, "edit desc")      ?
        return
    
    def _get_color_information(self):
        return
    
    def process_request(self, request):
        # idk how this is gonna get the information to determine which method to call so assuming string rn
        if request == "initialize":
            self._initialize_image()
            self._create_history_entry # save newly created image
        elif request == "export":
            self._export_image()
        elif request == "edit":
            self._edit()
            self._create_history_entry() # save current image version after edit
        elif request == "undo" or request == "redo":
            self._history_action(request)
        elif request == "color":
            self._get_color_information()
class Arguments:
    def __init__(self, image):
        self.args = {}
        self.args["image"] = image
        
    def add_selection(self, selection):
        self.args["image"] = selection
    
    # still want to explore other options for these
    # also they'll eventually be enums and stuff
    def add_filter(self, filter_name):
        self.args["filter"] = filter_name
    def add_shape(self, shape_name):
        self.args["shape"] = shape_name
    def add_color(self, color):
        self.args["color"] = color

    def get_args(self):
        return self.args
    
    
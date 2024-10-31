import Color

class Arguments:
    """Build a dictionary of arguments to be passed to Edit subclasses"""
    def __init__(self, image = None) -> None:
        self.args = {}
        if image:
            self.args["image"] = image
            
    def add_selection(self, selection) -> None:
        self.args["image"] = selection
    
    # eventually these will prob be enums and stuff
    def add_filter(self, filter_name: str) -> None:
        """Name of filter to apply"""
        self.args["filter"] = filter_name
    def add_amount(self, amount: float) -> None:
        """An amount, usually to inform a filter strength"""
        self.args["amount"] = amount
            
    def add_shape(self, shape_name: str) -> None:
        """Name of the chosen shape"""
        self.args["shape"] = shape_name
    def add_color(self, color: Color) -> None:
        """A Color object, usually to inform a shape's color"""
        self.args["color"] = color

    def get_args(self) -> None:
        return self.args
    
    
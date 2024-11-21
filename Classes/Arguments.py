from ArgumentType import ArgumentType as AT
from Selection import Selection

class Arguments:
    """Build a dictionary of arguments to be passed to Edit subclasses"""
    def __init__(self, image = None) -> None:
        self.args = {}
        if image:
            self.args[AT.AMOUNT] = image
            
    def add_image(self, image) -> bool:
        """Adds an image to args and returns True if it's not overwriting an existing image value; otherwise False"""
        key_already_existed = AT.IMAGE in self.args
        self.args[AT.IMAGE] = image
        return not key_already_existed
            
    def add_selection(self, selection: Selection) -> None:
        """Coordinates of selection"""
        self.args[AT.SELECTION] = selection
    
    # eventually these will prob be enums and stuff
    def add_filter(self, filter_name: str) -> None:
        """Name of filter to apply"""
        self.args[AT.FILTER] = filter_name
    def add_amount(self, amount: float) -> None:
        """An amount, usually to inform a filter strength"""
        self.args[AT.AMOUNT] = amount
            
    def add_shape(self, shape_name: str) -> None:
        """Name of the chosen shape"""
        self.args[AT.SHAPE] = shape_name
    def add_color(self, color: tuple[int, int, int]) -> None:
        """An RGB color tuple, usually to inform a shape's color"""
        self.args[AT.COLOR] = color

    def get_args(self) -> dict:
        return self.args
    
    def __str__(self) -> str:
        string = "Arguments:\n"
        for key in self.args:
            string += f"\t{str(key)[str(key).index(".")+1:].lower()}: {self.args[key]}"
        return string
            
    def __repr__(self) -> str:
        string = "Arguments()"
        for key in self.args:
            string += f".add_{str(key)[str(key).index(".")+1:].lower()}({self.args[key]})"
        return string
    
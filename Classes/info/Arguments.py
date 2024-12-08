from Classes.info.ArgumentType import ArgumentType as AT
from Classes.info.Selection import Selection
from Classes.image.Image import Image
from Classes.edit.draw.ShapeType import ShapeType

class Arguments:
    """Build a dictionary of arguments to be passed to Edit subclasses"""
    def __init__(self, image: Image = None) -> None:
        self.args = {}
        if image:
            self.args[AT.IMAGE] = image
            
    def add_image(self, image: Image) -> bool:
        """Adds an image to args and returns True if it's not overwriting an existing image value; otherwise False"""
        key_already_existed = AT.IMAGE in self.args
        self.args[AT.IMAGE] = image
        return not key_already_existed
            
    def add_selection(self, selection: Selection) -> bool:
        """Coordinates of actual selection"""
        self.args[AT.SELECTION] = selection
        return True
        
    def add_selection2(self, selection: Selection) -> bool:
        """Coordinates of selection2; e.g. shape draw area"""
        self.args[AT.SELECTION2] = selection
        return True
    
    # eventually these will prob be enums and stuff
    def add_filter(self, filter_type: AT) -> bool:
        """Name of filter to apply"""
        self.args[AT.FILTER] = filter_type
        return True
    
    def add_amount(self, amount: float) -> bool:
        """An amount, usually to inform a filter strength"""
        self.args[AT.AMOUNT] = amount
        return True
            
    def add_shape(self, shape_type: ShapeType) -> bool:
        """Name of the chosen shape"""
        self.args[AT.SHAPE] = shape_type
        return True
    
    def add_color(self, color: tuple[int, int, int]) -> bool:
        """An RGB color tuple, usually to inform the drawing color"""
        self.args[AT.COLOR] = color
        return True

    def add_size(self, dimensions: tuple[int, int]) -> bool:
        self.args[AT.SIZE] = dimensions
        return True

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
    
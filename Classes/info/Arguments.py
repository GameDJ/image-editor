from Classes.info.ArgumentType import ArgumentType as AT
from Classes.info.Selection import Selection
from Classes.image.Image import Image
from Classes.edit.draw.ShapeType import ShapeType
from typing import Self

class Arguments:
    """Build a dictionary of arguments to be passed to Edit subclasses"""
    def __init__(self, image: Image = None) -> None:
        self.args = {}
        if image:
            self.args[AT.IMAGE] = image
            
    def add_image(self, image: Image) -> Self:
        """Adds an image to args and returns True if it's not overwriting an existing image value; otherwise False"""
        self.args[AT.IMAGE] = image
        return self
            
    def add_selection(self, selection: Selection) -> Self:
        """Coordinates of actual selection"""
        self.args[AT.SELECTION] = selection
        return self
        
    def add_selection2(self, selection: Selection) -> Self:
        """Coordinates of selection2; e.g. shape draw area"""
        self.args[AT.SELECTION2] = selection
        return self
    
    # eventually these will prob be enums and stuff
    def add_filter(self, filter_type: AT) -> Self:
        """Name of filter to apply"""
        self.args[AT.FILTER] = filter_type
        return self
    
    def add_amount(self, amount: float) -> Self:
        """An amount, usually to inform a filter strength"""
        self.args[AT.AMOUNT] = amount
        return self
            
    def add_shape(self, shape_type: ShapeType) -> Self:
        """Name of the chosen shape"""
        self.args[AT.SHAPE] = shape_type
        return self
    
    def add_color(self, color: tuple[int, int, int]) -> Self:
        """An RGB color tuple, usually to inform the drawing color"""
        self.args[AT.COLOR] = color
        return self

    def add_size(self, dimensions: tuple[int, int]) -> Self:
        self.args[AT.SIZE] = dimensions
        return self
    
    def add_coord(self, coord: tuple[int, int]) -> Self:
        self.args[AT.COORD] = coord
        return self

    def get_args(self) -> dict:
        return self.args
    
    def __str__(self) -> str:
        string = "Arguments:"
        for key in self.args:
            string += f"\n\t{str(key)[str(key).index(".")+1:].lower()}: {self.args[key]}"
        return string
            
    def __repr__(self) -> str:
        string = "Arguments()"
        for key in self.args:
            string += f".add_{str(key)[str(key).index(".")+1:].lower()}({self.args[key]})"
        return string
    
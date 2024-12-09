from enum import Enum, auto

class ArgumentType(Enum):
    IMAGE = auto()
    # SELECTION: only for actual selections
    SELECTION = auto()
    # SELECTION2: for a second "selection"; for example:
    #   DuplicateSelection's target region  
    #   DrawShape's shape region
    SELECTION2 = auto()
    FILTER = auto()
    AMOUNT = auto()
    SHAPE = auto()
    COLOR = auto()
    SIZE = auto()
    COORD = auto()
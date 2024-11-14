from enum import Enum, auto

class FilterType(Enum):
    BLUR = auto()
    INVERT = auto()
    FLIP_HORIZONTAL = auto()
    FLIP_VERTICAL = auto()
    GRAYSCALE = auto()
    ADJUST_BRIGHTNESS = auto()
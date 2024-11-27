from enum import Enum, auto
from Classes.ArgumentType import ArgumentType

class FilterType(Enum):
    BLUR = auto()
    INVERT = auto()
    FLIP_HORIZONTAL = auto()
    FLIP_VERTICAL = auto()
    GRAYSCALE = auto()
    ADJUST_BRIGHTNESS = auto()

FilterInfo = {
    FilterType.BLUR: {
        "text": "Blur",
        "args": [ArgumentType.AMOUNT]
    },
    FilterType.INVERT: {
        "text": "Invert colors",
        "args": []
    },
    FilterType.FLIP_HORIZONTAL: {
        "text": "Flip Horizontal",
        "args": []
    },
    FilterType.FLIP_VERTICAL: {
        "text": "Flip Vertical",
        "args": []
    },
    FilterType.GRAYSCALE: {
        "text": "Convert to grayscale",
        "args": []
    },
    FilterType.ADJUST_BRIGHTNESS: {
        "text": "Adjust Brightness",
        "args": [ArgumentType.AMOUNT]
    }
}
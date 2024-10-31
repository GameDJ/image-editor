class Color:
    """Class to hold the rgb values of a color."""
    
    def __init__(self, red: int, green: int, blue: int):
        self.rgb = {}
        self.rgb["red"] = red
        self.rgb["green"] = green
        self.rgb["blue"] = blue
    
    def get_color_value(self) -> dict:
        return self.rgb
    
    def set_color_value(self, red: int, green: int, blue: int):
        self.rgb["red"] = red
        self.rgb["green"] = green
        self.rgb["blue"] = blue

from numpy import ndarray

class Renderer:
    def __init__(self, image: ndarray = []) -> None:
        self.image = image
        
    def render_image(self) -> None:
        pass
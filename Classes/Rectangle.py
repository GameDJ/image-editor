import Shape
import Image
import Arguments
import cv2

class Rectangle(Shape):
    def __init__(self, name: str = "Rectangle"):
        super().__init__(name)
    
    def apply_shape(self, image: Image, args: Arguments) -> Image:
        
        self.image = cv2.rectangle(self.image)
        
        return self.image
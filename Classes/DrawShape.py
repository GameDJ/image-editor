import Edit
import Image
import Arguments
import ShapeType
import Rectangle

class DrawShape(Edit):
    def __init__(self, image: Image):
        self.image = image

    def edit(self, shape_type: ShapeType, image: Image, args: Arguments)->Image:
        shape_type = args.get_args()["shape_type"]

        if shape_type == ShapeType.RECTANGLE:
            shape = Rectangle()

        return shape.apply_shape(self.image, args)
    
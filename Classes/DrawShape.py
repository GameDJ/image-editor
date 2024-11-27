from Edit import Edit
from Image import Image
from Arguments import Arguments
from ArgumentType import ArgumentType as AT
from ShapeType import ShapeType
from Rectangle import Rectangle
from Selection import Selection
import numpy as np

class DrawShape(Edit):
    @staticmethod
    def edit(args: Arguments) -> Image:
        # get the image and its array
        full_image: Image = args.get_args()[AT.IMAGE]
        full_image_array: np.ndarray = full_image.get_img_array()
        # get the selection and its bbox
        sel: Selection = args.get_args()[AT.SELECTION]
        sel_bbox: tuple[int, int, int, int] = sel.get_bbox()
        # get just the selected part of the image array
        image_edit_area = full_image_array[sel_bbox[1]:sel_bbox[3], sel_bbox[0]:sel_bbox[2]]

        # set the shape type
        shape_type = args.get_args()[AT.SHAPE]
        if shape_type == ShapeType.RECTANGLE:
            shape = Rectangle
        else:
            return None

        # get the color and apply the shape with that color
        color: tuple[int, int, int] = args.get_args()[AT.COLOR]
        image_edit_area = shape.apply_shape(image_edit_area, color)
        
        # Apply the edited selection area to the full image array
        full_image_array[sel_bbox[1]:sel_bbox[3], sel_bbox[0]:sel_bbox[2]] = image_edit_area
        full_image.set_img_array(full_image_array)
        return full_image
    
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
        """Draw a shape.
        Arguments:
        image -- Image to edit
        shape -- ShapeType of shape to apply
        selection -- (optional) marquee selection area to intersect with drawn shape in the final image
        selection2 -- selection area in which to apply the shape
        color -- RGB tuple to set the pixel values of the shape to
        
        Returns:
        The edited image.
        OR None, if the shape was outside selection bounds (no change to image).
        """
        # get the image and its array
        full_image: Image = args.get_args()[AT.IMAGE]
        full_image_array: np.ndarray = full_image.get_img_array()
        # get the actual selection (to be applied later)
        actual_sel_bbox: tuple[int, int, int, int] = None
        if AT.SELECTION in args.get_args():
            actual_sel: Selection = args.get_args()[AT.SELECTION]
            actual_sel_bbox = actual_sel.get_bbox()
        # get the shape selection area and its bbox
        shape_sel: Selection = args.get_args()[AT.SELECTION2]
        shape_sel_bbox: tuple[int, int, int, int] = shape_sel.get_bbox()
        # get just the selected part of the image array
        image_edit_area = full_image_array[shape_sel_bbox[1]:shape_sel_bbox[3], shape_sel_bbox[0]:shape_sel_bbox[2]]

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
        if actual_sel_bbox is not None:
            # check that at least part of the shape area's actually within selection bounds
            shape_start_is_after_sel_end = (shape_sel_bbox[0] > actual_sel_bbox[2] or shape_sel_bbox[1] > actual_sel_bbox[3])
            sel_start_is_after_shape_end = (actual_sel_bbox[0] > shape_sel_bbox[2] or actual_sel_bbox[1] > shape_sel_bbox[3])
            if shape_start_is_after_sel_end or sel_start_is_after_shape_end:
                return None
            # determine the intersecting bounds of the shape area and the actual selection (if applicable)
            combined_bbox = list(shape_sel_bbox)
            # this will be the offset in relation to the shape area's top left corner
            offset = [0, 0, shape_sel_bbox[2] - shape_sel_bbox[0], shape_sel_bbox[3] - shape_sel_bbox[1]]
            for i in range(4):
                if i <= 1:
                    max_bound = max(actual_sel_bbox[i], shape_sel_bbox[i])
                    combined_bbox[i] = max_bound
                    offset[i] = max_bound - shape_sel_bbox[i]
                else:
                    min_bound = min(actual_sel_bbox[i], shape_sel_bbox[i])
                    combined_bbox[i] = min_bound
                    offset[i] = min_bound - shape_sel_bbox[i-2]
            full_image_array[combined_bbox[1]:combined_bbox[3], combined_bbox[0]:combined_bbox[2]] = image_edit_area[offset[1]:offset[3], offset[0]:offset[2]]
        else:
            # no actual selection; simply apply the edited shape area
            full_image_array[shape_sel_bbox[1]:shape_sel_bbox[3], shape_sel_bbox[0]:shape_sel_bbox[2]] = image_edit_area
            
        full_image.set_img_array(full_image_array)
        return full_image
    
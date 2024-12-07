import PIL.Image
from Classes.info.History import History
from Classes.info.Arguments import Arguments
from Classes.info.ArgumentType import ArgumentType as AT
from Classes.edit.filter.FilterType import FilterType, FilterInfo
from Classes.edit.filter.Filters import Filters
from Classes.edit.draw.DrawShape import DrawShape
from Classes.edit.draw.ShapeType import ShapeType
from Classes.info.Selection import Selection
from Classes.image.Image import Image
from Classes.image.render.ImageRenderer import ImageRenderer
from Classes.image.render.BasicImageRenderer import BasicImageRenderer
from Classes.image.render.SelectionRenderer import SelectionRenderer
from Classes.image.render.ShapeRenderer import ShapeRenderer
from Classes.image.render.ZoomRenderer import ZoomRenderer
from Classes.edit.Crop import Crop
from Classes.edit.SizeEditor import SizeEditor
from Classes.edit.DuplicateSelection import DuplicateSelection
from Classes.image.ImageInitializer import ImageInitializer
from Classes.image.file.JpegImporter import JpegImporter
from Classes.image.file.PngImporter import PngImporter
from Classes.image.file.JpegExporter import JpegExporter
from Classes.image.file.PngExporter import PngExporter
from Classes.gui.GUI_Defaults import GUI_Defaults
import numpy as np
import PIL
import os.path

class RequestHandler:
    """Handles all requests."""
    
    def __init__(self):
        self.hist = History()
        self.selection = Selection()
        self.zoom_level = 1
    
    def create_canvas(self, width: int, height: int, color: tuple[int, int, int]) -> bool:
        """Returns True if blank canvas initialization successful (else False)"""
        creator = ImageInitializer()
        new_image = creator.create_blank_canvas(width, height, color)
        return self.initialize_image(new_image)
    
    def import_image(self, file_path: str) -> bool:
        """Returns True if image initialization successful (else False)"""
        # get just the file name from the whole path
        # file_name = file_path.split("/")[-1]
        # open the file as a PIL Image
        split_path = file_path.split(".")
        file_type = split_path[len(split_path) - 1].lower()
        importer = None
        if file_type == "png":
            importer = PngImporter()
        elif file_type == "jpeg" or file_type == "jpg":
            importer = JpegImporter()
        else:
            return False
        image = importer.import_image(file_path)
        if not image:
            return False
        self.file_path = file_path
        return self.initialize_image(image)
    
    def get_file_path(self) -> str:
        if hasattr(self, "file_path"):
            return self.file_path
        else:
            return None
    
    def initialize_image(self, image: Image) -> bool:
        # shrink image if it's too big
        height, width = image.get_img_array().shape[0:2]
        max_width = GUI_Defaults.IMAGE_MAX_WIDTH.value
        max_height = GUI_Defaults.IMAGE_MAX_HEIGHT.value
        # determine ratio of actual width/height to the max allowed
        maxwidth_ratio = width / max_width 
        maxheight_ratio = height / max_height
        # if at least one is greater, we must shrink
        if maxwidth_ratio > 1 or maxheight_ratio > 1:
            # determine which ratio is greater
            bigger_ratio = max(maxwidth_ratio, maxheight_ratio)
            # determine new dimensions
            new_width = int(width / bigger_ratio)
            new_height = int(height / bigger_ratio)
            # now shrink it
            args = Arguments()
            args.add_image(image)
            args.add_size((new_width, new_height))
            size_editor = SizeEditor()
            image = size_editor.edit(args)
        
        retVal = self._create_history_entry(image, "Create image")
        return retVal
    
    def export_image(self, save_pathname: str):
        split_path = save_pathname.split(".")
        file_type = split_path[len(split_path) - 1].lower()
        exporter = None
        if file_type == "png":
            exporter = PngExporter()
        elif file_type == "jpeg" or file_type == "jpg":
            exporter = JpegExporter()
        exporter.export_image(self.get_current_actual_image(), save_pathname)
        if os.path.isfile(save_pathname):
            return True
        else:
            return False
    
    def make_selection(self, start_coord: tuple[int, int], end_coord: tuple[int, int]) -> bool:
        # self.selection = Selection(start_coord, end_coord)

        #Bounds checking
        if not (start_coord[0] < 0 or start_coord[0] > len(self.get_current_actual_image().get_img_array()) or
                start_coord[1] < 0 or start_coord[1] > len(self.get_current_actual_image().get_img_array()[0]) or
                end_coord[0] < 0 or end_coord[0] > len(self.get_current_actual_image().get_img_array()) or
                 end_coord[1] < 0 or end_coord[1] > len(self.get_current_actual_image().get_img_array()[0])):        
        
            self.selection.set_bbox_from_coords(start_coord, end_coord)

        else:
            height, width = self.get_current_actual_image().get_img_array().shape[0:2]
            start_x_clamped = min(max(0, start_coord[0]), width)
            start_y_clamped = min(max(0, start_coord[1]), height)

            end_x_clamped = min(max(0, end_coord[0]), width)
            end_y_clamped = min(max(0, end_coord[1]), height)

            self.selection.set_bbox_from_coords((start_x_clamped, start_y_clamped), (end_x_clamped, end_y_clamped))

        return True


    def get_selection_bbox(self) -> tuple[int, int, int, int]:
        """Returns None if no bbox is set"""
        return self.selection.get_bbox()
        
    def clear_selection(self) -> bool:
        """Returns True if there was a bbox to clear, otherwise False"""
        cleared = self.selection.clear()
        return cleared
    
    def edit(self, args: Arguments) -> bool:
        # make a copy of the current image
        args.add_image(self.hist.get_current_img())
        # add selection, if there is one
        if self.selection.get_bbox() is not None:
            args.add_selection(self.selection)
        # edit the image
        if AT.FILTER in args.get_args():
            try:
                filter = Filters()
                edited_image = filter.edit(args)
            except Exception as e:
                raise e
            desc = FilterInfo[args.get_args()[AT.FILTER]]["text"]
        elif AT.SHAPE in args.get_args():
            draw_shape = DrawShape()
            edited_image = draw_shape.edit(args)
            desc = args.get_args()[AT.SHAPE].value
        # add the edited image to history, with the filter text as the change description
        if edited_image is not None:
            return self._create_history_entry(edited_image, desc)
        return False
    
    def get_current_actual_image(self) -> Image:
        return self.hist.get_current_img()
    
    def get_image_dimensions(self) -> tuple[int, int]:
        return self.hist.get_current_img().get_img_array().shape[0:2]
    
    def history_undo(self) -> bool:
        return self.hist.undo()
        
    def history_redo(self) -> bool:
        return self.hist.redo()
        
    def history_set_index(self, index: int):
        self.hist.set_index(index)
        
    def _create_history_entry(self, image: Image, desc: str) -> bool:
        return self.hist.add_record(image, desc)
        
    def history_descriptions(self) -> list[tuple[int, str]]:
        return self.hist.get_entry_descriptions()
    
    def zoom_change(self, delta: int) -> int:
        """Change the zoom level (cannot be 0), and return the new level
        
        Arguments:
        delta -- +1 to zoom in, -1 to zoom out
        """
        self.zoom_level += delta
        if self.zoom_level == 0:
            self.zoom_level += delta        
        return self.zoom_level
        
    def get_zoom_level(self) -> int:
        if hasattr(self, self.zoom_level):
            return self.zoom_level
    
    def is_active_image(self) -> bool:
        """Returns True if history has a current image"""
        return self.hist.is_active_image()
    
    def history_get_index(self) -> int:
        return self.hist.get_index()
    
    def get_render_image(self, args: Arguments = None) -> Image:
        render_image = BasicImageRenderer(self.hist.get_current_img())
        if args is None:
            args = Arguments()
        args.add_image(render_image)
        
        if self.zoom_level != 1:
            args.add_amount(self.zoom_level)
            args.add_size((GUI_Defaults.IMAGE_MAX_WIDTH.value, GUI_Defaults.IMAGE_MAX_HEIGHT.value))
            # zoom the render_image
            render_image = ZoomRenderer(render_image, args)
            # make a copy of selection and edit its coordinates based on zoom


        if AT.SHAPE in args.get_args():
            # render a shape while it's being dragged
            render_image = ShapeRenderer(render_image, args)
            
        if self.selection.get_bbox() is not None:
            # render selection box
            render_image = SelectionRenderer(render_image, self.selection)
        return render_image.render_image()
    
    def get_color_at_pixel(self, x: int, y: int) -> list[int, int, int]:
        if x < 0 or y < 0:
            raise ValueError
        return self.get_current_actual_image().get_img_array()[y][x]
    
    def crop(self) -> bool:
        args = Arguments()
        # make a copy of the current image
        args.add_image(self.hist.get_current_img())
        # add selection, if there is one
        if self.selection.get_bbox() is None:
            return False
        args.add_selection(self.selection)
        crop = Crop()
        edited_image = crop.edit(args)
        if edited_image is not None:
            return self._create_history_entry(edited_image, "Crop")
        return False

    def resize(self, dimensions: tuple[int, int]) -> bool:
        args = Arguments()
        args.add_image(self.hist.get_current_img())
        args.add_size(dimensions)
        size_editor = SizeEditor()
        resized_image = size_editor.edit(args)
        if resized_image is not None:
            return self._create_history_entry(resized_image, "Resize")
        return False
    
    def duplicate_selection(self, start_coord: tuple[int, int]) -> bool:
        args = Arguments()
        # make a copy of the current image
        args.add_image(self.hist.get_current_img())
        # add selection, if there is one
        if self.selection.get_bbox() is None:
            return False
        args.add_selection(self.selection)
        
        # add selection to duplicate to
        orig_selection = self.selection.get_bbox()
        height, width = self.hist.get_current_img().get_img_array().shape[0:2]
        end_coord = (min(orig_selection[2] - orig_selection[0] + start_coord[0], width), min(orig_selection[3] - orig_selection[1] + start_coord[1], height))
        args.add_selection2(Selection(start_coord, end_coord))
        
        duplicate = DuplicateSelection()
        edited_image = duplicate.edit(args)
        if edited_image is not None:
            return self._create_history_entry(edited_image, "Duplicate Selection")
        return False
        

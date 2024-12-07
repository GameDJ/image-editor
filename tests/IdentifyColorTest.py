#Addison Casner

import unittest
import numpy as np
import sys
sys.path.append("../image-editor")
from Classes.RequestHandler import RequestHandler
from Classes.image.Image import Image


class TestIdentifyColorFromImage(unittest.TestCase):
    def test_valid_pixel(self):
        self.handler = RequestHandler()
        dummy_image_array = np.array([
            [[0, 0, 255], [0, 255, 0], [255,0,0]],
            [[255, 128, 0], [255, 255, 0], [255, 0, 255]],
            [[255, 255, 255], [128, 128, 128], [0, 0, 0]]
            ])

            #[blue, green, red]
            #[orange, yellow, purple]
            #[white, gray, black]
        
        dummy_image = Image(dummy_image_array)
        self.handler.hist.add_record(dummy_image, "Dummy image for testing")
        color = self.handler.get_color_at_pixel(0,0)
        self.assertListEqual(color, (0,0,255))
    
    def test_edge_pixel(self):
        self.handler = RequestHandler()
        dummy_image_array = np.array([
            [[0, 0, 255], [0, 255, 0], [255,0,0]],
            [[255, 128, 0], [255, 255, 0], [255, 0, 255]],
            [[255, 255, 255], [128, 128, 128], [0, 0, 0]]
            ])

            #[blue, green, red]
            #[orange, yellow, purple]
            #[white, gray, black]
        
        dummy_image = Image(dummy_image_array)
        self.handler.hist.add_record(dummy_image, "Dummy image for testing")
        color = self.handler.get_color_at_pixel(2,1)
        print(color)
        self.assertTupleEqual(color, (255,0,255))

    def test_invalid_pixel_out_of_bounds(self):
        self.handler = RequestHandler()
        dummy_image_array = np.array([
            [[0, 0, 255], [0, 255, 0], [255,0,0]],
            [[255, 128, 0], [255, 255, 0], [255, 0, 255]],
            [[255, 255, 255], [128, 128, 128], [0, 0, 0]]
            ])

            #[blue, green, red]
            #[orange, yellow, purple]
            #[white, gray, black]
        
        dummy_image = Image(dummy_image_array)
        self.handler.hist.add_record(dummy_image, "Dummy image for testing")
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(3, 0)
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(0, 3)
    
    def test_negative_pixel_index(self):
        self.handler = RequestHandler()
        dummy_image_array = np.array([
            [[0, 0, 255], [0, 255, 0], [255,0,0]],
            [[255, 128, 0], [255, 255, 0], [255, 0, 255]],
            [[255, 255, 255], [128, 128, 128], [0, 0, 0]]
            ])

            #[blue, green, red]
            #[orange, yellow, purple]
            #[white, gray, black]
        
        dummy_image = Image(dummy_image_array)
        self.handler.hist.add_record(dummy_image, "Dummy image for testing")
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(-1, 0)
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(0, -1)

    def test_no_active_image(self):
        self.handler = RequestHandler()
        self.handler.hist = None
        with self.assertRaises(AttributeError):
            self.handler.get_color_at_pixel(0,0)

if __name__ == "__main__":
    unittest.main()
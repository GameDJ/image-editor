#Addison Casner

import unittest
import numpy as np
from Classes.RequestHandler import RequestHandler
from Classes.image.Image import Image


class TestIdentifyColorFromImage(unittest.TestCase):

    def setup(self):
        self.handler = RequestHandler()
        dummy_image_array = np.array([
            [[0, 0, 255], [0, 255, 0], [255,0,0]],
            [[255, 128, 0], [255, 255, 0], [255, 0, 255]],
            [[255, 255, 255], [128, 128, 128], [0, 0, 0]]
            ],dytpe=np.uint8)

            #[blue, green, red]
            #[orange, yellow, purple]
            #[white, gray, black]
        
        dummy_image = Image(dummy_image_array)
        self.handler.hist.add_record(dummy_image, "Dummy image for testing")


    def test_valid_pixel(self):
        color = self.handler.get_color_at_pixel(0,0)
        self.assertEqual(color, (0,0,255))
    
    def test_edge_pixel(self):
        color = self.handler.get_color_at_pixel(1,2)
        self.assertEqual(color, (255,0,255))

    def test_invalid_picel_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(3, 0)
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(0, 3)
    
    def test_negative_pixel_index(self):
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(-1, 0)
        with self.assertRaises(IndexError):
            self.handler.get_color_at_pixel(0, -1)

    def test_no_active_image(self):
        self.handler.hist = None
        with self.assertRaises(AttributeError):
            self.handler.get_color_at_pixel(0,0)

if __name__ == "__main__":
    unittest.main()
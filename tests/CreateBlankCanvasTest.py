# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\CreateBlankCanvasTest.py

import unittest
import sys
sys.path.append("../image-editor")
from Classes.image.ImageInitializer import ImageInitializer

class CreateBlankCanvasTest(unittest.TestCase):
    def test_valid_arguments(self):
        initializer = ImageInitializer()
        self.assertEqual(initializer.create_blank_canvas(10, 10, (78, 62, 128)), True)
    
    def test_negative_size(self):
        initializer = ImageInitializer()
        self.assertEqual(initializer.create_blank_canvas(-10, -10, (78, 62, 128)), True)
    
    def test_zero_size(self):
        initializer = ImageInitializer()
        self.assertRaises(ValueError, initializer.create_blank_canvas (0, 0, (78, 62, 128)))
        
if __name__ == '__main__':
    unittest.main()
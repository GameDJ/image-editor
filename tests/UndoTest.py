# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\UndoTest.py
# Quinn Pulley

import unittest
import sys
sys.path.append("../image-editor")
from Classes.info.History import History
from Classes.image.Image import Image
import numpy as np

class TestUndo(unittest.TestCase):
    def test_empty_history(self):
        hist = History()
        self.assertEqual(hist.undo(), False)
        
    def test_history_with_one_entry(self):
        hist = History()
        image_array = np.full((10, 10, 3), (78, 62, 128), dtype=np.uint8)
        hist.add_record(Image(image_array), "")
        self.assertEqual(hist.undo(), False)
    
    def test_history_with_multiple_entries(self):
        hist = History()
        for x in range(3):
            image_array = np.full((10, 10, 3), (78, 62, 128), dtype=np.uint8)
            hist.add_record(Image(image_array), "")
        self.assertEqual(hist.undo(), True)
    
    
if __name__ == '__main__':
    unittest.main()
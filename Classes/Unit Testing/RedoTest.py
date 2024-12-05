# def redo(self) -> bool:
#     if (self.index < len(self.array_history)-1):
#         self.index += 1
#         return True
#     return False

import unittest
from Classes.History import History
from Classes.Image import Image
import numpy as np

class TestRedo(unittest.TestCase):    
    def test_empty_history(self):
        hist = History()
        self.assertEqual(hist.redo(), False)
        
    def test_history_with_no_undone_entries(self):
        hist = History()
        for x in range(3):
            image_array = np.full((10, 10, 3), (78, 62, 128), dtype=np.uint8)
            hist.add_record(Image(image_array), "")
        self.assertEqual(hist.redo(), False)
    
    def test_history_with_one_undone_entry(self):
        hist = History()
        for x in range(3):
            image_array = np.full((10, 10, 3), (78, 62, 128), dtype=np.uint8)
            hist.add_record(Image(image_array), "")
        hist.undo()
        self.assertEqual(hist.redo(), True)
    
    def test_history_with_multiple_undone_entries(self):
        hist = History()
        for x in range(3):
            image_array = np.full((10, 10, 3), (78, 62, 128), dtype=np.uint8)
            hist.add_record(Image(image_array), "")
        for x in range(2):
            hist.undo()
        self.assertEqual(hist.redo(), True)
    
    
if __name__ == '__main__':
    unittest.main()
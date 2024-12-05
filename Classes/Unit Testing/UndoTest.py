# def undo(self) -> bool:
#     if (self.index > 0):
#         self.index -= 1
#         return True
#     return False

# does he want use case testing to use objects in context or can i create a dummy history?

import unittest
from Classes.History import History
from Classes.Image import Image
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
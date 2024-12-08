# MUST BE RUN FROM image-editor FOLDER AS: python .\tests\SelectAreaTest.py
# Addison Casner

import unittest
import sys
sys.path.append("../image-editor")

from Classes.RequestHandler import RequestHandler



class TestSelectArea(unittest.TestCase):
    
    def test_in_bounds_selection(self):
        handler = RequestHandler()
        handler.create_canvas(10, 10, (78, 62, 128))
        self.assertEqual(handler.make_selection( (0,0), (5,8)) , True)

    def test_out_of_bounds(self):
        handler = RequestHandler()
        handler.create_canvas(10, 10, (78, 62, 128))
        self.assertEqual(handler.make_selection( (-1,-1,), (1000,8000)) , True)


if __name__ == '__main__':
    unittest.main()
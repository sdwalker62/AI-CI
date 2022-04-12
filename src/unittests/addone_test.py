from scripts.test_functions import add_one, subtract_one

import unittest

class MathTests(unittest.TestCase):

    def test_add_one(self):
        self.assertEqual(add_one(1), 2)

    def test_subtract_one(self):
        self.assertEqual(subtract_one(155), 154)
        

"""
This file contains various toy test cases for testing out dagger.io
"""
if __name__ == '__main__':
    unittest.main() # pragma: no cover
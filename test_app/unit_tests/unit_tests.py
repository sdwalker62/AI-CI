import unittest
import sys
import os

# Append main directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from test_functions import add_one

"""
This file contains various toy test cases for testing out dagger.io
"""

class MathTests(unittest.TestCase):

    def test_add_one(self):
        self.assertEqual(add_one(1), 2)


if __name__ == '__main__':
    unittest.main()
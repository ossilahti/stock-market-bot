import unittest
import sys
import json
from formulas import percentage_growth

class TestFormulas(unittest.TestCase):
    def test_percentage_growth(self):
        self.assertAlmostEqual(percentage_growth(50, 25), 100)
        self.assertAlmostEqual(percentage_growth(2, 3), -33.33)
        self.assertAlmostEqual(percentage_growth('jono', 3), 'Formatting problem')
        self.assertAlmostEqual(percentage_growth(1, 0), 'Dividing by zero')
        self.assertAlmostEqual(percentage_growth('',''), 'Formatting problem')
        self.assertAlmostEqual(percentage_growth(None, None), 'Formatting problem')


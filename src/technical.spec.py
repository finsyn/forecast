# technical analysis utility functions 
# tests

from technical import asy 
from pandas import DataFrame
import math
import unittest

# some mocked closing prices
mock_close = DataFrame(
    [ 1, 2, 3, 4, 5 ],
    columns = ['close']
)
    
class TestTechAnalysis(unittest.TestCase):

    def test_asy(self):
        mars = asy(2, mock_close['close'])

        last_true = (math.log(5.0/4.0) + math.log(4.0/3.0))/2.0

        self.assertEqual(round(last_true, 5), round(mars[4], 5))

        self.assertTrue(math.isnan(mars.iloc[0]))
        self.assertTrue(math.isnan(mars.iloc[1]))
        
if __name__ == '__main__':
    unittest.main()

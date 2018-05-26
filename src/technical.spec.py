# technical analysis utility functions 
# tests

from technical import asy 
from pandas import DataFrame
import math
import unittest

# some mocked closing prices
mock_close = DataFrame(
    [ 10, 11, 14, 12, 40 ],
    columns = ['close']
)
    
class TestTechAnalysis(unittest.TestCase):

    def test_asy(self):
        mars = asy(2, mock_close['close'])
        self.assertTrue(math.isnan(mars.iloc[0]))
        self.assertTrue(math.isnan(mars.iloc[1]))
        self.assertTrue(mars.iloc[4] > mars.iloc[3])
        
if __name__ == '__main__':
    unittest.main()

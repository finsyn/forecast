# technical analysis utility functions 
# tests

from technical import asy, psy
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

    def test_psy(self):
        psyr = psy(3, mock_close['close'])
        self.assertTrue(math.isnan(psyr.iloc[0]))
        self.assertTrue(math.isnan(psyr.iloc[1]))
        self.assertEqual(2./3., psyr[2])
        self.assertEqual(1, psyr[3])
        self.assertEqual(1, psyr[4])
       
if __name__ == '__main__':
    unittest.main()

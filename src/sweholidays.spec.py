from sweholidays import get_trading_close_holidays
import unittest

holidays_2018 = [
    '01-01', '01-06',
    '03-30',
    '04-02', 
    '05-01', '05-10',
    '06-06',
    '12-24', '12-25', '12-26', '12-31'
]

class TestSwedishHolidays(unittest.TestCase):

    def test_get(self):
        holidays = get_trading_close_holidays(2018).values
        holidays = map(lambda x: str(x)[:10], holidays)
        holidays = filter(lambda x: x[:4] == '2018', holidays)

        holidays_real = map(lambda x: '2018-%s' % x, holidays_2018)

        self.assertEqual(holidays, holidays_real)
        
if __name__ == '__main__':
    unittest.main()

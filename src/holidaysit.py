from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
from pandas.tseries.offsets import Easter, Day
import datetime as dt

# Based on schedule at 
# http://markets.on.nytimes.com/research/markets/holidays/holidays.asp?display=market&timeOffset=0&exchange=MIL
class ITTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1),
        Holiday('Good Friday', month=1, day=1, offset=[Easter(), Day(-2)]),
        Holiday('Easter Monday', month=1, day=1, offset=[Easter(), Day(1)]),
        Holiday('Ascesion Day', month=1, day=1, offset=[Easter(), Day(39)]),
        Holiday('Workers Day', month=5, day=1),
        Holiday('Assumption Day', month=8, day=15),
        Holiday('Christmas', month=12, day=24),
        Holiday('ChristmasDay', month=12, day=25),
        Holiday('ChristmasSecondDay', month=12, day=26),
        Holiday('NewYearsEve', month=12, day=31)
    ]


def get_trading_close_holidays(year):
    inst = ITTradingCalendar()

    return inst.holidays(dt.datetime(year-10, 12, 31), dt.datetime(year, 12, 31))

from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
from pandas.tseries.offsets import Easter, Day
import datetime as dt

class HKTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1),

        # some tricky asian holidays, seems complicated to calculate

        # chinese new year
        Holiday('CNY2017-3', year=2017, month=1, day=30),
        Holiday('CNY2017-4', year=2017, month=1, day=31),
        Holiday('CNY2018-1', year=2018, month=2, day=16),
        Holiday('CNY2018-4', year=2018, month=2, day=19),

        # Ching Ming festival
        Holiday('CMF2017', year=2017, month=4, day=4),
        Holiday('CMF2018', year=2018, month=4, day=5),

        # Buddah birthday
        Holiday('BBD2017', year=2017, month=5, day=3),
        Holiday('BBD2018', year=2018, month=5, day=22),

        # Tuen Ng Day
        Holiday('TND2017', year=2017, month=5, day=30),
        Holiday('TND2018', year=2018, month=6, day=18),

        # Day after mid-autumn festival
        Holiday('DAMAF2017', year=2017, month=10, day=5),
        Holiday('DAMAF2018', year=2018, month=9, day=25),

        Holiday('Good Friday', month=1, day=1, offset=[Easter(), Day(-2)]),
        Holiday('Easter Monday', month=1, day=1, offset=[Easter(), Day(1)]),
        Holiday('WorkersDay', month=5, day=1),
        Holiday('NationalDay', month=10, day=1),
        Holiday('ChristmasDay', month=12, day=25),
        Holiday('ChristmasSecondDay', month=12, day=26)
    ]

def get_trading_close_holidays(year):
    inst = HKTradingCalendar()

    return inst.holidays(dt.datetime(year-10, 12, 31), dt.datetime(year, 12, 31))

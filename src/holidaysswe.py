from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
from pandas.tseries.offsets import Easter, Day
import datetime as dt

class SETradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1),
        Holiday('Trettondagjul', month=1, day=6),
        Holiday('Good Friday', month=1, day=1, offset=[Easter(), Day(-2)]),
        Holiday('Easter Monday', month=1, day=1, offset=[Easter(), Day(1)]),
        Holiday('Ascesion Day', month=1, day=1, offset=[Easter(), Day(39)]),
        Holiday('WorkersDay', month=5, day=1),
        Holiday('NationalDay', month=6, day=6),
        Holiday('Christmas', month=12, day=24),
        Holiday('ChristmasDay', month=12, day=25),
        Holiday('ChristmasSecondDay', month=12, day=26),
        Holiday('NewYearsEve', month=12, day=31)
    ]


def get_trading_close_holidays(year):
    inst = SETradingCalendar()

    return inst.holidays(dt.datetime(year-10, 12, 31), dt.datetime(year, 12, 31))

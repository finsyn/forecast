from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
import datetime as dt

class SETradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
        Holiday('NationalDay', month=6, day=6, observance=nearest_workday),
        Holiday('Christmas', month=12, day=24, observance=nearest_workday),
        Holiday('ChristmasDay', month=12, day=25, observance=nearest_workday),
        Holiday('ChristmasSecondDay', month=12, day=26, observance=nearest_workday),
        Holiday('NewYearsEve', month=12, day=31, observance=nearest_workday),
        Holiday('WorkersDay', month=5, day=1, observance=nearest_workday)
    ]


def get_trading_close_holidays(year):
    inst = SETradingCalendar()

    return inst.holidays(dt.datetime(year-10, 12, 31), dt.datetime(year, 12, 31))

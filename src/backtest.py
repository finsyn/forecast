import numpy as np
import pandas as pd
from load import load_quotes_daily, read_data_csv
from sweholidays import get_trading_close_holidays
from matplotlib import pyplot

leverage = 4
cap = cap_safe = 10000

res = np.genfromtxt('data/test-output.csv', delimiter=',')
y_h = res[0]

n_lags = len(y_h)
df = read_data_csv('data/indexes.csv')


o = pd.DataFrame()
c = df.loc[df['id'] == 'market-index_OMX30']
o['change'] = (c.c - c.o)/c.o

# remove dates when STO is closed
index_range = pd.date_range(
            end=pd.datetime(2018, 3, 30),
            periods=n_lags,
            freq=pd.offsets.BDay(),
            holidays=get_trading_close_holidays(2018)
            )

o = o.reindex(index_range)

o = o.interpolate(limit_direction='both')
o = o.tail(n_lags)

y = o.values
y_h = y_h.astype(bool)
cap_hist = []
cap_hist_safe = []

for i in range(0, n_lags):
    multiplier = leverage if y_h[i] else -1 * leverage
    cap *= 1 + multiplier * y[i]
    cap_safe *= 1 + leverage * y[i]
    cap_hist.append(cap.copy())
    cap_hist_safe.append(cap_safe.copy())


print(len(cap_hist))
pyplot.plot(range(0, n_lags), cap_hist, cap_hist_safe)
pyplot.show()

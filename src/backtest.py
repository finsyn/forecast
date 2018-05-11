import numpy as np
import pandas as pd
from load import load_quotes_daily, read_data_csv
from sweholidays import get_trading_close_holidays
from matplotlib import pyplot

leverage_long = 1
leverage_ava = 8
leverage_ig = 100

cap_init = 10000

res = np.genfromtxt('data/test-output.csv', delimiter=',')
y_h = res[0]

n_lags = len(y_h)
df = read_data_csv('data/indexes.csv')


o = pd.DataFrame()
c = df.loc[df['id'] == 'market-index_OMX30']
o['diff'] = c.c - c.o
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

change_hist = o['change'].values
diffs_hist = o['diff'].values
pred_up_hist = y_h.astype(bool)

def run_ava(cap_init, changes, predictions, leverage): 
    cap_hist = []
    cap = cap_init
    for i in range(0, n_lags):
        multiplier = leverage if predictions[i] else -1 * leverage
        cap *= 1 + multiplier * changes[i] 
        cap_hist.append(cap.copy())
    return cap_hist

def run_ig(cap_init, diffs, predictions, leverage): 
    cap_hist = []
    cap = cap_init
    for i in range(0, n_lags):
        multiplier = leverage if predictions[i] else -1 * leverage
        cap += multiplier * diffs[i]
        cap -= leverage * 0.5
        cap_hist.append(cap.copy())
    return cap_hist


def run_long(cap_init, changes, leverage): 
    cap_hist = []
    cap = cap_init
    for i in range(0, n_lags):
        cap *= 1 + leverage * changes[i]
        cap_hist.append(cap.copy())
    return cap_hist

cap_hist_safe = run_long(cap_init, change_hist, leverage_long)
cap_hist_ava = run_ava(cap_init, change_hist, pred_up_hist, leverage_ava)
cap_hist_ig = run_ig(cap_init, diffs_hist, pred_up_hist, leverage_ig)

x = range(0, n_lags)
pyplot.plot(x, cap_hist_ava, 'g-', label='Avanza certificates')
pyplot.plot(x, cap_hist_ig, 'r-', label='IG CFD:s')
pyplot.plot(x, cap_hist_safe, 'b-', label='Long x1')

pyplot.legend()
pyplot.show()

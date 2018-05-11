import numpy as np
import pandas as pd
from load import load_quotes_daily, read_data_csv
from sweholidays import get_trading_close_holidays
from matplotlib import pyplot

leverage_long = 1 
leverage_ava = 8
leverage_ig = 200
ig_stop_limit = 5

cap_init = 10000

res = np.genfromtxt('data/test-output.csv', delimiter=',')
y_h = res[0]

n_lags = len(y_h)
df = read_data_csv('data/indexes.csv')

o = pd.DataFrame()
c = df.loc[df['id'] == 'market-index_OMX30']
o['diff'] = c.c - c.o
o['close'] = c.c
o['open'] = c.o
o['low'] = c.l
o['high'] = c.h
o['change'] = (c.c - c.o)/c.o

# remove dates when STO is closed
index_range = pd.bdate_range(
            end=pd.datetime(2018, 5, 10),
            periods=n_lags,
            freq='C',
            holidays=get_trading_close_holidays(2018)
            )

o = o.reindex(index_range)

o = o.interpolate(limit_direction='both')
o = o.tail(n_lags)

change_hist = o['change'].values
diffs_hist = o['diff'].values
close_hist = o['close'].values
opens_hist = o['open'].values
lows_hist = o['low'].values
highs_hist = o['high'].values
pred_up_hist = y_h.astype(bool)

def run_ava(cap_init, changes, predictions, leverage): 
    cap_hist = []
    cap = cap_init
    for i in range(0, n_lags):
        multiplier = leverage if predictions[i] else -1 * leverage
        cap *= 1 + multiplier * changes[i] 
        # product fee 
        cap *= 1 - 0.0006
        # spread fee
        cap *= 1 - 0.0012
        cap_hist.append(cap.copy())
    return cap_hist

def run_ig(cap_init, diffs, opens, lows, highs, predictions, leverage, stop_limit):
    cap_hist = []
    cap = cap_init
    for i in range(0, n_lags):
        pred = predictions[i]
        multiplier = leverage if pred else -1 * leverage
        # stop limit
        if (
            (opens[i] - lows[i]  > stop_limit and pred) or
            (highs[i] - opens[i] > stop_limit and not pred)
        ):
            cap -= leverage * stop_limit
        else:
            cap += multiplier * diffs[i]
        # spread fee
        cap -= leverage * 0.5
        cap_hist.append(cap.copy())
    return cap_hist


def run_long(cap_init, closes, leverage): 
    cap_hist = []
    cap = cap_init
    cap_hist.append(cap)
    for i in range(1, n_lags):
        cap *= 1 + (closes[i]/closes[i-1] - 1) * leverage
        cap_hist.append(cap.copy())
    return cap_hist

cap_hist_safe = run_long(cap_init, close_hist, leverage_long)
cap_hist_ava = run_ava(cap_init, change_hist, pred_up_hist, leverage_ava)
cap_hist_ig = run_ig(cap_init, diffs_hist, opens_hist, lows_hist, highs_hist,  pred_up_hist, leverage_ig, ig_stop_limit)

label_ava = 'BULL/BEAR AVA X%s' % leverage_ava
label_ig = 'IG CFD %s SEK/point stop-limit: %s' % (leverage_ig, ig_stop_limit)
label_long = 'No forecast: AVANZA zero' 

x = range(0, n_lags)
pyplot.plot(x, cap_hist_ava, 'g-', label=label_ava)
pyplot.plot(x, cap_hist_ig, 'r-', label=label_ig)
pyplot.plot(x, cap_hist_safe, 'b-', label=label_long)

pyplot.title('Using forecast for daily long/short positions (fees included)')
pyplot.xlabel('Business days')
pyplot.ylabel('SEK')
pyplot.legend()
pyplot.show()

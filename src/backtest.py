import numpy as np
from pandas import read_csv, TimeGrouper, concat
from joblib import load
import copy
from os import environ, getenv
# from sweholidays import get_trading_close_holidays

# args
id = environ['TARGET_CFD_ID']
id_backtest = environ['BACKTEST_CFD_ID']

# config
leverage_ig = 20
ig_stop_limit = 6 
cap_init = 6000

# load persisted setup
features_df = read_csv('outputs/%s-features.csv' % id, header=None)
features_idx = features_df[1].values.flatten()
model = load('model-rf.joblib')

def predict(df):
    sample = df.values[features_idx]
    df['prediction'] = model.predict_proba([sample])

feat = read_csv(
    'data/%s-feat.csv' % id,
    header=0,
    index_col=0,
    parse_dates=True
)
quote = read_csv(
    'data/%s-backtest.csv' % id_backtest,
    header=0,
    index_col=0,
    parse_dates=True
)
feat['probdown'] = model.predict_proba(feat.values[:,features_idx])[:,0]

def dayReturn(day):
    if day.empty: return None
    date = day.index.date[0]
    prediction = feat.loc[date]['probdown']
    startprice = day.iloc[0]['open'] 
    for index, row in day.iterrows():
        if (prediction > 0.5 and row['low'] < startprice - ig_stop_limit):
            return - leverage_ig * (ig_stop_limit + 0.8)
        if (prediction <= 0.5 and row['high'] > startprice + ig_stop_limit):
            return - leverage_ig * (ig_stop_limit + 0.8)
    sign = -1 if (prediction > 0.5) else 1
    return (startprice - day.iloc[-1]['open']) * leverage_ig * sign

returns = (quote
           .groupby(TimeGrouper('D'))
           .apply(dayReturn))

print(returns)
print(returns.sum())

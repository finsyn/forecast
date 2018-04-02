from pandas import isnull, datetime, date_range, read_csv, concat, to_datetime, DataFrame
import re
import numpy as np
from sklearn import preprocessing
from sklearn.externals import joblib

# open, close -> return
ret = lambda x,y: np.log(y/x) #Log return 
scale = lambda x: x/x.max()

def read_data_csv(csvfile):
    df = read_csv(
            csvfile,
            header=0,
            index_col=0
            )
    df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime
    return df

def load_quotes_daily(df):
    securities = list(set(df['id'].values))

    # securities = ['market-index_OMX30', 'market-index_VIX']
    print('loading daily quotes for %s entities' % len(securities))
    
    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()
        if (s_id == 'market-index_OMX30'):
            o['c'] = c.c
            o['l_2_h'] = ret(c.l,c.h)
        if (s_id == 'market-index_SP500'):
            o['v'] = c.v
        if (s_id != 'market-index_XLRE'):
            o['c_2_o'] = ret(c.o,c.c)
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.index.name = 'date'
    return agg 

def load_insiders(csvfile):
    df = read_csv(csvfile, header=0, index_col=0)
    print('loading insiders net sum for %s days' % len(df))
    df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime
    securities = list(set(df['id'].values))

    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()
        o['buy'] = c['buy']
        o['sell'] = c['sell']
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg = agg.apply(lambda x: x/x.max(), axis=1)
    agg.fillna(0.0, axis=1, inplace=True)
    agg.index.name = 'date'

    return agg

def load_shorts(csvfile):
    df = read_csv(csvfile, header=0, index_col=0)
    df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime

    print('loading short positions for %s days' % len(df))
    securities = list(set(df['id'].values))

    cols, names = list(), list()

    for s_id in securities:

        o = DataFrame()
        o['shortChange'] = df.loc[df['id'] == s_id]['totalDiff']
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.fillna(0.0, axis=1, inplace=True)
    agg.index.name = 'date'

    return agg

def add_calendar_events(df):
    # a column for market opening awareness 
    df['isMonday'] = (df.index.weekday == 0).astype(int)
    df['isFriday'] = (df.index.weekday == 4).astype(int)

def load_features():
    df_quotes_raw = read_data_csv('data/quotes.csv')
   
    df_quotes = load_quotes_daily(df_quotes_raw)
   
    df = concat([df_quotes], axis=1, join='outer')

    # period of interest
    # Be aware that yahoo only have open AND close price of OMX30 since 2009-01-01 
    start = datetime(2016, 10, 4)
    end = datetime(2018, 3, 30)
    index_range = date_range(start, end)
    df.reindex(index_range)

    # remove dates when STO is closed
    df = df.loc[df['market-index_OMX30-c'] > 0]
    df.drop(columns=['market-index_OMX30-c'], inplace=True)

    df = df.interpolate()

    scaler = preprocessing.MinMaxScaler()
    df = DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    joblib.dump(scaler, 'scaler.save')
    df['market-index_OMX30-c_2_o'] = df_quotes['market-index_OMX30-c_2_o']

    add_calendar_events(df)
    return df

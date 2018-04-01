from pandas import isnull, datetime, date_range, read_csv, concat, to_datetime, DataFrame
import re
import numpy as np
from sklearn import preprocessing

# open, close -> return
ret = lambda x,y: np.log(y/x) #Log return 
scale = lambda x: x/x.max()

def load_quotes_daily(csvfile):
    df = read_csv(
            csvfile,
            header=0,
            index_col=0,
            names=['date', 'id', 'c', 'o','h','l','v'] 
            )
    df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime
    securities = list(set(df['id'].values))

    # securities = ['market-index_OMX30', 'market-index_VIX']
    print('loading daily quotes for %s entities' % len(securities))
    
    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()
        if (s_id == 'market-index_OMX30'):
            o['c'] = c.c
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


def load_features():
    quotesfile = 'data/quotes.csv'
    insidersfile = 'data/insiders.csv'
    shortsfile = 'data/shorts.csv'
    
    df_quotes = load_quotes_daily(quotesfile)
    df_insiders = load_insiders(insidersfile)
    df_shorts = load_shorts(shortsfile)

    # period of interest
    # Be aware that yahoo only have open AND close price of OMX30 since 2009-01-01 
    start = datetime(2016, 10, 4)
    end = datetime(2018, 3, 30)
    index = date_range(start, end)
    
    df = concat([df_quotes], axis=1, join='outer')

    df = df.reindex(index)

    # remove dates when STO is closed
    df = df.loc[df['market-index_OMX30-c'] > 0]
    df.drop(columns=['market-index_OMX30-c'], inplace=True)

    df = df.interpolate()

    scaler = preprocessing.MinMaxScaler()
    df = DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    df['market-index_OMX30-c_2_o'] = df_quotes['market-index_OMX30-c_2_o']

    # a column for market opening awareness 
    df['isMonday'] = (df.index.weekday == 0).astype(int)
    df['isFriday'] = (df.index.weekday == 4).astype(int)

    print(df.corr())
    return df

from pandas import isnull, datetime, date_range, read_csv, concat, to_datetime, DataFrame, offsets
import re
import numpy as np
from sklearn import preprocessing
from sklearn.externals import joblib
from sweholidays import get_trading_close_holidays

# open, close -> return
ret = lambda x,y: np.log(y/x) #Log return 

def read_data_csv(csvfile):
    df = read_csv(
            csvfile,
            header=0,
            index_col=0
            )
    df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime
    return df

def load_groups(df):
    securities = list(set(df['id'].values))

    # securities = ['market-index_OMX30', 'market-index_VIX']
    print('loading daily quotes for %s entities' % len(securities))
    
    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()
        o['numDown'] = np.log(1+c.numDown)
        o['volume'] = np.log(1+c.volume)
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.index.name = 'date'
    return agg 


def load_quotes_daily(df):
    securities = list(set(df['id'].values))

    # securities = ['market-index_OMX30', 'market-index_VIX']
    print('loading daily quotes for %s entities' % len(securities))
    
    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()
        if (s_id != 'market-index_XLRE'):
            o['up'] = (ret(c.o,c.c) > 0.0).astype(int)
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.index.name = 'date'
    return agg 

def load_insiders(df):
    securities = list(set(df['id'].values))

    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()
        o['buy'] = c['buy']
        o['sell'] = c['sell']
        # o['netBuy'] = ((c['buy'] - c['sell']) > 0).astype(int)
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names
    agg = agg.resample('D', label='right').pad()
    agg.index.name = 'date'

    return agg

def load_shorts(df):
    print('loading short positions for %s days' % len(df))
    securities = list(set(df['id'].values))

    cols, names = list(), list()

    for s_id in securities:

        o = DataFrame()
        o['shortChange'] = ((df.loc[df['id'] == s_id]['totalDiff']) > 0.0).astype(int)
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.fillna(0.5, axis=1, inplace=True)
    agg.index.name = 'date'

    return agg

def add_calendar_events(df):
    # a column for market opening awareness 
    df['isMonday'] = (df.index.weekday == 0).astype(int)
    df['isFriday'] = (df.index.weekday == 4).astype(int)
    # df['isMonthStart'] = (df.index.is_month_end).astype(int)
    # df['isQuarterStart'] = (df.index.is_quarter_start).astype(int)

def load_features():
    df_indexes_raw = read_data_csv('data/indexes.csv')
    df_groups_raw = read_data_csv('data/groups.csv')
    df_shorts_raw = read_data_csv('data/shorts.csv')
    df_insiders_raw = read_data_csv('data/insiders.csv')
   
    df_indexes = load_quotes_daily(df_indexes_raw)
    df_groups = load_groups(df_groups_raw)
    df_shorts = load_shorts(df_shorts_raw)
    df_insiders = load_insiders(df_insiders_raw)
   
    df = concat([df_indexes], axis=1, join='outer')

    # period of interest
    # Be aware that yahoo only have open AND close price of OMX30 since 2009-01-01 
    # We only want days when stockholm stock exchange is open
    start = datetime(2012, 1, 1)
    end = datetime(2018, 3, 30)
    index_range = date_range(
            start,
            end,
            freq=offsets.BDay(),
            holidays=get_trading_close_holidays(2018)
            )
    df = df.reindex(index_range)

    df = df.interpolate(limit_direction='both')

    # add_calendar_events(df)
    df['target'] = df['market-index_OMX30-up']

    scaler = preprocessing.MinMaxScaler()
    df = DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    joblib.dump(scaler, 'scaler.save')

    return df

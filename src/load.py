from pandas import isnull, datetime, bdate_range, read_csv, read_json, concat, to_datetime, DataFrame, offsets
import numpy as np
from technical import asy, rlog, ma, psy
from sklearn import preprocessing
from sklearn.externals import joblib
import holidaysswe
import holidayshk

def read_data_csv(csvfile):
    df = read_csv(
            csvfile,
            header=0,
            index_col=0
            )
    df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime
    return df

def load_target(df):
    o = DataFrame()
    o['target'] = (rlog(df['c'],df['o']) > 0.0).astype(int)
    o.index.name = 'date'
    return o

# A substitute for OBV indicator since we dont have
# OMX30 trade volume
def load_volume(df):
    o = DataFrame()
    o['obv'] = df['v'] 
    o.index.name = 'date'
    return o

# Indicators from Mingyue Qiu and Yu Song
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4873195/#!po=48.9130
def load_indicators(df):
    quotes = list(set(df['id'].values))

    print('loading daily technical indicators (type 2) for %s entities' % len(quotes))
    
    cols, names = list(), list()

    for s_id in quotes:

        data = df.loc[df['id'] == s_id]
        c = data['c']

        o = DataFrame()
        o['ma5'] = ma(5, c)
        o['ma12'] = ma(12, c)
        o['bias6'] = (c - ma(6, c)) / ma(6, c)
        o['psy12'] = psy(12, c)
        o['asy5'] = asy(5, c)
        o['asy4'] = asy(4, c)
        o['asy3'] = asy(3, c) 
        o['asy2'] = asy(2, c)
        o['asy1'] = asy(1, c)

        # homemade volatility feature
        # high/low not always available in dataset
        if ('h' in data.columns):
            h = data['h']
            l = data['l']
            o['ma5hl'] = rlog(l, h)

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

def load_calendar_events(df):
    # a column for market opening awareness 
    o = DataFrame()
    o['isMonday'] = (df.index.weekday == 0).astype(int)
    o['isFriday'] = (df.index.weekday == 4).astype(int)
    o.index = df.index

    return o

def load_quotes_daily(df):
    securities = list(set(df['id'].values))

    # securities = ['market-index_OMX30']
    print('loading daily quotes for %s entities' % len(securities))
    
    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()

        # o['up'] = (rlog(c.o,c.c) > 0.0).astype(int)
        o['rlog'] = rlog(c.o,c.c)
        # o['psy12'] = psy(12, c.c)
        # o['asy1'] = asy(1, c.c)
        # o['bigdiff'] = (abs(rlog(c.o,c.c) > 0.01)).astype(int)
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names
 
    agg.index.name = 'date'
    return agg 

def get_trading_close_holidays(country_code):
    holidays = {
        'HK': holidayshk.get_trading_close_holidays,
        'SE': holidaysswe.get_trading_close_holidays
    }
    return holidays[country_code](2018)

def load_features(service_id, country_code, date_from, date_to):

    df_cfds_raw = read_data_csv('data/%s.csv' % service_id)
    df_indicators = load_indicators(df_cfds_raw)

    df_indexes_raw = read_data_csv('data/indexes.csv')
    df_indexes = load_indicators(df_indexes_raw)
    df_calendar_events = load_calendar_events(df_cfds_raw)

    df_commodities_raw = read_data_csv('data/commodities.csv')
    df_commodities = load_indicators(df_commodities_raw)

    df_target = load_target(df_cfds_raw)

    df = concat([df_indicators, df_indexes, df_commodities, df_target], axis=1, join='outer')

    # period of interest
    # Be aware that yahoo only have open AND close price of OMX30 since 2009-01-01 
    # We only want days when market of target security/index is open
    start = to_datetime(date_from)
    end = to_datetime(date_to)
    index_range = bdate_range(
            start,
            end,
            freq='C',
            holidays=get_trading_close_holidays(country_code)
            )
    df = df.reindex(index_range)

    df = df[12:]

    print('[INFO] these features contains NaN entries')
    print(df.isna().sum())
    # df = df.dropna()

    df = df.interpolate()

    scaler = preprocessing.MinMaxScaler()
    # scaler = preprocessing.StandardScaler()
    df[df_indicators.columns] = scaler.fit_transform(df[df_indicators.columns])
    df[df_commodities.columns] = scaler.fit_transform(df[df_commodities.columns])
    df[df_indexes.columns] = scaler.fit_transform(df[df_indexes.columns])
    joblib.dump(scaler, 'outputs/%s-scaler.save' % service_id)

    return df

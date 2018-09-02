from pandas import isnull, datetime, bdate_range, read_csv, read_json, concat, to_datetime, DataFrame, offsets
import numpy as np
from technical import asy, rlog, ma, psy
from sklearn import preprocessing
from sklearn.externals import joblib
import holidaysswe
import holidayshk
import holidaysit

def read_data_csv(csvfile):
    df = read_csv(
            csvfile,
            header=0,
            index_col=0
            )
    df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime
    return df

# Target label
def load_binary(df, colname):
    o = DataFrame()
    o[colname] = (rlog(df['c'],df['o']) > 0.0).astype(int)
    o.index.name = 'date'
    return o

# Indicators from Mingyue Qiu and Yu Song
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4873195/#!po=48.9130
def load_indicators(df):
    quotes = sorted(list(set(df['id'].values)))

    print('loading daily technical indicators (type 2) for %s entities' % len(quotes))
    
    cols, names = list(), list()

    for s_id in quotes:

        data = df.loc[df['id'] == s_id]
        c = data['c']

        o = DataFrame()
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
            # o['ma5hl'] = rlog(l, h)

        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.index.name = 'date'
    return agg 

def get_trading_close_holidays(country_code):
    holidays = {
        'HK': holidayshk.get_trading_close_holidays,
        'SE': holidaysswe.get_trading_close_holidays,
        'IT': holidaysit.get_trading_close_holidays
    }
    return holidays[country_code](2018)

def load_features(service_id, country_code, date_from, date_to):

    target_data_file = 'data/%s.csv' % service_id

    raw_files = [
        target_data_file,
        'data/indexes.csv'
        # unfortunately we dont have any daily reporting on quandl data
        # 'data/commodities.csv'
    ]

    df_features = []

    # populate feature columns
    for file in raw_files:
        df_raw = read_data_csv(file)
        df = load_indicators(df_raw)
        df_features.append(df)

    df_target = load_binary(read_data_csv(target_data_file), 'target')

    # join features and target dfs
    df = concat(df_features + [df_target], axis=1, join='outer')

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

    # because one indicator needs 12 starting days
    df = df[12:]

    print('[INFO] these features contains NaN entries')
    print(df.isna().sum())

    df = df.interpolate()

    # scale all features
    scaler = preprocessing.MinMaxScaler()
    df.iloc[:,0:-1] = scaler.fit_transform(df.iloc[:,0:-1])
    joblib.dump(scaler, 'outputs/%s-scaler.save' % service_id)

    return df

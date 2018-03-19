from pandas import datetime, date_range, read_csv, concat, to_datetime, DataFrame
import re
import numpy as np

# open, close -> return
ret = lambda x,y: np.log(y/x) #Log return 

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
        o['c_2_o'] = ret(c.o,c.c)
        # Add target attr 
        if (s_id == 'market-index_OMX30'):
            o['c_2_o_dbl'] = ret(c.o, c.c)
        # VIX is already "normalized
        if (s_id == 'market-index_VIX'):
            o['c'] = c.c
        # o['h_2_o'] = ret(c.o,c.h)
        # o['l_2_o'] = ret(c.o,c.l)
        # o['c_2_h'] = ret(c.h,c.c)
        # o['h_2_l'] = ret(c.h,c.l)
        if (re.search('security_', s_id)):
            o['vol']   = c.v
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

    agg.fillna(0.0, axis=1, inplace=True)
    agg.index.name = 'date'

    return agg

def load_kpi(csvfile):
    df = read_csv(csvfile, header=0, index_col=0)
    # df = df.pivot(index='month')
    print(df.values)
    # df.index = to_datetime(df.index,format='%Y-%m-%d') # Set the indix to a datetime

    # print('loading short positions for %s days' % len(df))
    # securities = list(set(df['id'].values))

    # cols, names = list(), list()

    # for s_id in securities:

    #     o = DataFrame()
    #     o['shortChange'] = df.loc[df['id'] == s_id]['totalDiff']
    #     cols.append(o)
    #     names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    # agg = concat(cols, axis=1)
    # agg.columns = names

    # agg.fillna(0.0, axis=1, inplace=True)
    # agg.index.name = 'date'

    # return agg



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
    # kpifile = 'data/kpi.csv'
    df_quotes = load_quotes_daily(quotesfile)
    df_insiders = load_insiders(insidersfile)
    df_shorts = load_shorts(shortsfile)
    # df_kpi = load_kpi(kpifile)

    # period of interest
    # Be aware that yahoo only have open AND close price of OMX30 since 2009-01-01 
    start = datetime(2016, 7, 1)
    end = datetime(2018, 2, 27)
    index = date_range(start, end)
    
    df = concat([df_quotes, df_shorts, df_insiders], axis=1, join='outer')
    df = df.reindex(index)
    # remove weekends
    df = df[df.index.dayofweek < 5]
    df = df.interpolate()
    df.fillna(0.0, axis=1, inplace=True)
    # a column for market opening awareness 
    df['isMonday'] = (df.index.weekday == 0).astype(int)
    return df

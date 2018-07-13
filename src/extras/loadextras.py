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



from pandas import read_csv, concat, to_datetime

def load_quotes_daily(csvfile):
    df = read_csv(csvfile, header=0, index_col=0)
    features = list(set(df['id'].values))

    print('loading daily quotes for %s shares' % len(features))

    df = df.drop(['volume'], axis=1)

    cols, names = list(), list()

    for feature in features:
        curr = df.loc[df['id'] == feature]
        curr = curr.drop(['id'], axis=1)
        curr = curr.interpolate()
        curr.index = to_datetime(curr.index)
        curr = curr[~curr.index.duplicated(keep='first')]

        # get relative change
        curr['change'] = (curr['close'] - curr['open']) / curr['open']
        curr = curr.drop(['close', 'open'], axis=1)
        cols.append(curr)
        names += [('%s-%s' % (feature, col_name)) for col_name in curr.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.interpolate(inplace=True)
    agg.fillna(0.0, axis=1, inplace=True)
    agg.index.name = 'date'

    return agg

def load_insiders(csvfile):
    df = read_csv(csvfile, header=0, index_col=0)
    print('loading insiders net sum for %s days' % len(df))
    df.index = to_datetime(df.index)
    return df

def load_features():
    quotesfile = 'data/quotes.csv'
    insidersfile = 'data/insiders.csv'
    df_quotes = load_quotes_daily(quotesfile)
    df_insiders = load_insiders(insidersfile)
    # df_weekly = load_quotes_weekly(quotesfile)
    # limit time scope
    # agg = agg.ix['2009-01-01':]
    df = concat([df_quotes, df_insiders], axis=1, join='inner')
    return df

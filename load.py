from pandas import read_csv, concat

df = read_csv('weekly.csv', header=0, index_col=0)
features = list(set(df['id'].values))

print('loading %s features' % len(features))

df = df.drop(['weekOpen'], axis=1)

cols, names = list(), list()

for feature in features:
    curr = df.loc[df['id'] == feature]
    curr = curr.drop(['id'], axis=1)
    curr = curr.interpolate()
    cols.append(curr)
    names += [('%s-%s' % (feature, col_name)) for col_name in curr.columns.values]

agg = concat(cols, axis=1)
agg.columns = names

agg.interpolate(inplace=True)
agg.fillna(0.0, axis=1, inplace=True)
agg.index.name = 'date'

agg = agg.ix['2009-01-01':]
agg.to_csv('results/weekly.csv')

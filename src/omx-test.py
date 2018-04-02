from load import load_features
from extract import query
from pandas import read_csv, DataFrame, concat
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
import numpy as np
import re

df = query('queries/groups.sql')
df.to_csv('data/groups.csv')

# open, close -> return
ret = lambda x,y: np.log(y/x) #Log return 


def load_groups(df):
    securities = list(set(df['id'].values))

    # securities = ['market-index_OMX30', 'market-index_VIX']
    print('loading daily quotes for %s entities' % len(securities))
    
    cols, names = list(), list()

    for s_id in securities:

        c = df.loc[df['id'] == s_id]
        o = DataFrame()
        o['numDown'] = c.numDown
        cols.append(o)
        names += [('%s-%s' % (s_id, col_name)) for col_name in o.columns.values]

    agg = concat(cols, axis=1)
    agg.columns = names

    agg.index.name = 'date'
    return agg 


df = read_csv('data/groups.csv', header=0, index_col=0)
df = load_groups(df)
print(df)
# change this to filter out what columns in the data to show
# cols = list(filter(lambda x: re.search('market', x), df.columns))
cols = df.columns
print(cols)
values = df[cols].values

n_plots_max = 16
n_plots = np.clip(values.shape[1], 0, n_plots_max)
groups = list(range(0,n_plots))
i = 1

# plot each column
pyplot.figure()
for group in groups:
	pyplot.subplot(len(groups), 1, i)
	pyplot.plot(values[:, group])
	pyplot.title(cols[group], y=0.5, loc='right')
	i += 1

pyplot.show()

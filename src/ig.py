import matplotlib as mp
# Headless
mp.use('Agg')

import matplotlib.pyplot as plt
from pandas import isnull, datetime, bdate_range, read_csv, read_json, concat, to_datetime, DataFrame, offsets
import numpy as np
import re
from os import environ

# actual opening price
df = read_csv(
    'data/ig-history.csv',
    header=0,
    index_col=0,
    converters={
        'PL Amount': lambda x: float(x.replace(',', '')),
        'Size': lambda x: float(re.sub(r"^-$", '0', x)),
        'Open level': lambda x: float(x.replace('-', '0'))
    },
    usecols=['Date', 'Transaction type', 'Open level', 'Size', 'PL Amount'])

id = environ['TARGET_CFD_ID'],

# only get relevant transactions, i.e stoplos premium and win/loss
df = df[df['Transaction type'].isin(['Handel', 'WITH'])]
df.drop(['Transaction type'], axis=1,inplace=True)

# create a proper time index
df.index.names = ['date']
df.index = to_datetime(df.index,format='%d/%m/%y') # Set the indix to a datetime

# gather transactions on the same date
df = df.groupby('date')['PL Amount', 'Open level', 'Size'].agg('sum')
print(df)

# theoretical (from api)
df2 = read_csv('data/%s.csv' % id, header=0, index_col=0, usecols=['date', 'o', 'c'])
df2.index = to_datetime(df2.index,format='%Y-%m-%d') # Set the indix to a datetime

# join
res = concat([df2, df], axis=1, join='inner')
res['bet'] = (res['Size'] > 0.0).astype(int)
res['dir'] = (res['c'] - res['o'] > 0).astype(int)
res['correct'] = (res['dir'] == res['bet']).astype(int)
res['openGoodDiff'] = (res['o'] - res['Open level']) * res['Size']
res['dayDiff'] = abs(res['c'] - res['o'])
res['diff'] = res['o'] - res['Open level']
res['mon'] = res['PL Amount']
res['revenue'] = res[res['PL Amount'] > 0]['PL Amount']
res['sum'] = res['PL Amount'].cumsum()

# cleanup
res.drop(['o', 'c', 'Open level', 'Size', 'PL Amount'], axis=1, inplace=True)

# plot monetary results
title = '%s performance so far' % id
filename = 'plots/%s-results.png' % id

# get cummulative monetary sum
ts = res.values[:,7] 
# add a starting point
ts = np.insert(ts, 0, 0)
plt.figure(figsize=(18, 18))  # in inches
plt.title(title)
plt.plot(ts)
plt.savefig(filename)

# print aggregate statistics
print(res.shape)
print(res)
print(res.apply(np.sum))

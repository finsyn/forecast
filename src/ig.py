from pandas import isnull, datetime, bdate_range, read_csv, read_json, concat, to_datetime, DataFrame, offsets
import numpy as np

# actual opening price
df = read_csv(
    'data/ig-history.csv',
    header=0,
    index_col=0,
    usecols=['Date', 'Open level', 'Size', 'PL Amount'])

df['bet'] = (df['Size'] > 0.0).astype(int)
df.index.names = ['date']
df.index = to_datetime(df.index,format='%d/%m/%y') # Set the indix to a datetime

# theoretical (from api)
df2 = read_csv('data/cfds.csv', header=0, index_col=0, usecols=['date', 'o', 'c'])
df2.index = to_datetime(df2.index,format='%Y-%m-%d') # Set the indix to a datetime

# join
res = concat([df2, df], axis=1, join='inner')
res['dir'] = (res['c'] - res['o'] > 0).astype(int)
res['correct'] = (res['dir'] == res['bet']).astype(int)
res['openGoodDiff'] = (res['o'] - res['Open level']) * res['Size']
res['dayDiff'] = abs(res['c'] - res['o'])
res['diff'] = res['o'] - res['Open level']
res['mon'] = res['PL Amount']

res.drop(['o', 'c', 'Open level', 'Size', 'PL Amount'], axis=1, inplace=True)
print(res.shape)
print(res)
print(res.apply(np.sum))

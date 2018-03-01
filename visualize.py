from pandas import read_csv
from matplotlib import pyplot
# load dataset
df = read_csv('weekly.csv', header=0, index_col=0)
omx30 = df.loc[df['id'] == 'market-index_OMX30']
values = omx30.values

groups = list(range(1,2))
i = 1

# plot each column
pyplot.figure()
for group in groups:
	pyplot.subplot(len(groups), 1, i)
	pyplot.plot(values[:, group])
	pyplot.title(df.columns[group], y=0.5, loc='right')
	i += 1

pyplot.show()

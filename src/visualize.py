from pandas import read_csv
from matplotlib import pyplot
# load dataset
df = read_csv('data/training.csv', header=0, index_col=0)
values = df.values

groups = list(range(0,24))
i = 1

# plot each column
pyplot.figure()
for group in groups:
	pyplot.subplot(len(groups), 1, i)
	pyplot.plot(values[:, group])
	pyplot.title(df.columns[group], y=0.5, loc='right')
	i += 1

pyplot.show()

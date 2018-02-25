from pandas import read_csv
from matplotlib import pyplot
# load dataset
dataset = read_csv('omx-v002.csv', header=0, index_col=0)
values = dataset.values

groups = list(range(7))
i = 1

# plot each column
pyplot.figure()
for group in groups:
	pyplot.subplot(len(groups), 1, i)
	pyplot.plot(values[:, group])
	pyplot.title(dataset.columns[group], y=0.5, loc='right')
	i += 1

pyplot.show()

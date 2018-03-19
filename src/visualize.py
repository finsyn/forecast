from pandas import read_csv
from matplotlib import pyplot
import numpy as np
import re
# load dataset
df = read_csv('data/training.csv', header=0, index_col=0)
# change this to filter out what columns in the data to show
cols = list(filter(lambda x: re.search('market', x), df.columns))
# cols = df.columns
print(cols)
values = df[cols].values

n_plots_max = 12
n_plots = np.clip(values.shape[1]-1, 0, n_plots_max)
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

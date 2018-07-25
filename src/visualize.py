import matplotlib as mp
# Headless
mp.use('Agg')


from pandas import read_csv
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
import numpy as np
import re
from os import environ
# load dataset
id = environ['TARGET_CFD_ID']
df = read_csv('data/%s-feat.csv' % id, header=0, index_col=0)
# change this to filter out what columns in the data to show
# cols = list(filter(lambda x: re.search('market', x), df.columns))
cols = df.columns
print(cols)
values = df[cols].values

n_plots_max = 50 
n_plots = np.clip(values.shape[1], 0, n_plots_max)
groups = list(range(0,n_plots))
i = 1

# plot each column
title = '%s model features' % id
filename = 'plots/%s-features.png' % id

plt.figure(figsize=(18, 18))  # in inches
plt.title(title)
for group in groups:
	plt.subplot(len(groups), 1, i)
	plt.plot(values[:, group])
	plt.title(cols[group], y=0.5, loc='right')
	i += 1

plt.savefig(filename)

from pandas import read_csv
from utils import series_to_supervised 

dataset = read_csv('omx.csv', header=0, index_col=0)
values = dataset.values
# ensure all data is float
values = values.astype('float32')
# frame as supervised learning
reframed = series_to_supervised(values, 1, 1)
# drop columns we don't want to predict
reframed.drop(reframed.columns[[4,5,6]], axis=1, inplace=True)
print(reframed.head())

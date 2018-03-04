from pandas import DataFrame
from pandas import concat

def get_train_data (data, target, n_lags=1, n_pred_steps=1):

    df = DataFrame(data)

    df_y = df[target]

    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_lags, 0, -1):
        cols.append(df.shift(i))
        names += [('%s(t-%d)' % (name, i)) for name in df.columns.values]

    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_pred_steps):
        cols.append(df_y.shift(-i))
        if i == 0:
            names += ['%s(t)' % target]
        else:
            names += [('%s(t+%d)' % (target, i))] 

    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    print(agg.shape)
    # interpolate some null values
    # agg.interpolate(inplace=True)
    # drop rows with NaN values
    agg.dropna(inplace=True)
    print(agg.shape)

    return agg

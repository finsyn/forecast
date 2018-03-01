from pandas import DataFrame
from pandas import concat

def get_train_data (data, target, n_lags=1, n_pred_steps=1):

    df = DataFrame(data)

    is_feature_col = lambda col: col != target
    features = list(filter(is_feature_col, df.columns.values))

    def col_name_to_idx (name): 
        return list(df.columns.values).index(target)

    def col_idx_to_name (idx): 
        return list(df.columns.values)[idx]

    df_y = df[target]
    df_x = df.drop(df.columns[[col_name_to_idx(target)]], axis=1)

    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_lags, 0, -1):
        cols.append(df_x.shift(i))
        names += [('%s(t-%d)' % (name, i)) for name in features]

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
    agg.interpolate(inplace=True)
    # drop rows with NaN values
    agg.dropna(inplace=True)
    print(agg.shape)

    return agg

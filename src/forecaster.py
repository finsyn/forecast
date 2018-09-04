from pandas import datetime, bdate_range, offsets, concat, read_csv
from extract import query
from load import load_indicators, get_trading_close_holidays
import numpy as np
from keras.models import load_model
from datetime import datetime, timedelta 
from sklearn import preprocessing
from sklearn.externals import joblib

def forecast(id, cc, cfd_opt):

    cfds_raw = query('queries/cfds.sql', cfd_opt)
    indexes_raw = query('queries/indexes.sql')

    cfds = load_indicators(cfds_raw)
    indexes = load_indicators(indexes_raw)

    df = concat([cfds, indexes], axis=1, join='outer')

    # remove dates when STO is closed
    # up until yesterday since that is the last day from which
    # we have all data
    # get 5 periods so we have something to interpolate between in case
    # of missing values due to e.g US market close
    index_range = bdate_range(
                end=datetime.now().date() - timedelta(1),
                periods=5,
                freq='C',
                holidays=get_trading_close_holidays(cc)
                )
    print(index_range)
    df = df.reindex(index_range)

    # after interpolation we only need one lag
    df = df.interpolate(limit_direction='both')
    df = df.tail(1)
    print(df)

    # normalize values
    scaler = joblib.load('outputs/%s-scaler.save' % id)
    df = scaler.transform(df)

    # extract wanted features
    features_df = read_csv('outputs/%s-features.csv' % id, header=None)
    features_idx = features_df[1].values.flatten()
    sample = df[:,features_idx]
    print(features_df[0].values)
    print(sample)

    # forecast
    model = load_model('outputs/%s-model.h5' % id)
    pred_probs = model.predict(sample)[0]
    pred_prob = np.amax(pred_probs)
    pred_idx = np.argmax(pred_probs, axis=-1)

    directions = [ 'DOWN', 'UP' ]
    pred_direction = directions[pred_idx]
    
    return (pred_direction, pred_prob)

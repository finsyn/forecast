from pandas import datetime, date_range, offsets
from extract import query
from load import load_quotes_daily
import numpy as np
from keras.models import load_model
from datetime import datetime, timedelta 
from sweholidays import get_trading_close_holidays

def forecast(n_lags, query_path):
    quotes_df_raw = query(query_path)
    quotes_df = load_quotes_daily(quotes_df_raw)

    # remove dates when STO is closed
    # up until yesterday since that is the last day from which
    # we have all data
    index_range = date_range(
                end=datetime.now().date() - timedelta(1),
                periods=n_lags,
                freq=offsets.BDay(),
                holidays=get_trading_close_holidays(2018)
                )

    df = quotes_df.reindex(index_range)

    df = df.interpolate(limit_direction='both')
    df = df.tail(n_lags)

    df['target'] = df['market-index_OMX30-up']

    model = load_model('model.h5')
    sample = df.values.reshape((1, n_lags, len(df.columns)))

    pred_probs = model.predict(sample)[0]
    pred_prob = np.amax(pred_probs)
    pred_idx = np.argmax(pred_probs, axis=-1)

    directions = [ 'DOWN', 'UP' ]
    pred_direction = directions[pred_idx]
    
    return (pred_direction, pred_prob)

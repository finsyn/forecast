from pandas import datetime, date_range, offsets, concat
from extract import query
from load import load_indicators, load_target
import numpy as np
from keras.models import load_model
from datetime import datetime, timedelta 
from sweholidays import get_trading_close_holidays

def forecast(query_path):
    quotes_df_raw = query(query_path)
    quotes_df = load_indicators(quotes_df_raw)
    target_df = load_target(quotes_df_raw)

    df = concat([quotes_df, target_df], axis=1, join='outer')
    # remove dates when STO is closed
    # up until yesterday since that is the last day from which
    # we have all data
    index_range = date_range(
                end=datetime.now().date() - timedelta(1),
                periods=1,
                freq=offsets.BDay(),
                holidays=get_trading_close_holidays(2018)
                )

    df = df.reindex(index_range)

    df = df.interpolate(limit_direction='both')
    df.drop(['target'], axis=1, inplace=True)

    print(df)
    model = load_model('model.h5')
    sample = df.values

    pred_probs = model.predict(sample)[0]
    pred_prob = np.amax(pred_probs)
    pred_idx = np.argmax(pred_probs, axis=-1)

    directions = [ 'DOWN', 'UP' ]
    pred_direction = directions[pred_idx]
    
    return (pred_direction, pred_prob)

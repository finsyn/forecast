from pandas import isnull, datetime, date_range, read_csv, concat, to_datetime, DataFrame
from extract import query
from load import load_quotes_daily, add_calendar_events
from sklearn.externals import joblib
import numpy as np
from keras.models import load_model

quotes_df_raw = query('queries/quotes.sql')
quotes_df = load_quotes_daily(quotes_df_raw)

# remove dates when STO is closed
df = quotes_df.loc[quotes_df['market-index_OMX30-c'] > 0]
df.drop(columns=['market-index_OMX30-c'], inplace=True)

df = df.interpolate()
df = df.tail(3)

scaler = joblib.load('scaler.save') 
df = DataFrame(scaler.transform(df), columns=df.columns, index=df.index)

add_calendar_events(df)

print(df)
model = load_model('model.h5')
sample = df.values.reshape((1, 3, 22))
print(sample)
pred_probs = model.predict(sample)
pred_prob = np.amax(pred_probs)
pred_idx = np.argmax(pred_prob, axis=-1)

directions = [ 'DOWN', 'UP' ]
pred_direction = directions[pred_idx]

print('I think OMX30 will go %s tomorrow with %s probability' % (pred_direction, pred_prob))

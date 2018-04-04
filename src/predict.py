from forecaster import forecast 

n_lags = 254 
pred_direction, pred_prob = forecast(n_lags, 'queries/indexes.sql')
print('I think OMX30 will go %s tomorrow with %s probability' % (pred_direction, pred_prob))

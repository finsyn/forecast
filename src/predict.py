from forecaster import forecast 

pred_direction, pred_prob = forecast('queries/cfds.sql')
print('I think OMX30 will go %s tomorrow with %s probability' % (pred_direction, pred_prob))

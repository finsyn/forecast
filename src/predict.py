from forecaster import forecast 
from os import environ

id = environ['TARGET_CFD_ID']
cc = environ['TARGET_COUNTRY']

cfd_opt = {
    'service_id': id,
    'timezone': environ['TIMEZONE'],
    'time_from': environ['TIME_FROM'],
    'time_to': environ['TIME_TO']
}

pred_direction, pred_prob = forecast(id, cc, cfd_opt)

print(
    'I think %s will go %s tomorrow with %s probability' % 
    (id, pred_direction, pred_prob)
)

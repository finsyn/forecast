from load import load_features
from extract import query
from pandas import concat
from os import environ

id = environ['TARGET_CFD_ID']

cfd_opt = {
    'service_id': id,
    'timezone': environ['TIMEZONE'],
    'time_from': environ['TIME_FROM'],
    'time_to': environ['TIME_TO']
}

cfds = query('queries/cfds.sql', cfd_opt)
cfds.to_csv('data/%s.csv' % id)

features = load_features(id)
features.to_csv('data/%s-feat.csv' % id)

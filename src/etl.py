from load import load_features
from extract import query
from pandas import concat
from os import environ

id = environ['TARGET_CFD_ID']
id_bt = environ['BACKTEST_CFD_ID']
cc = environ['TARGET_COUNTRY']
load_from = environ['TRAIN_FROM']
load_to = environ['TRAIN_TO']

## target data
print('ETL target CFD')
cfd_opt = {
    'service_id': id,
    'timezone': environ['TIMEZONE'],
    'time_from': environ['TIME_FROM'],
    'time_to': environ['TIME_TO']
}

cfds = query('queries/cfds.sql', cfd_opt)
cfds.to_csv('data/%s.csv' % id)

## backtest data
print('ETL backtest CFD')
cfd_bt_opt = {
    'service_id': id_bt,
    'timezone': environ['TIMEZONE'],
    'time_from': environ['TIME_FROM'],
    'time_to': environ['TIME_TO']
}

cfds_bt = query('queries/cfds-backtest.sql', cfd_bt_opt)
cfds_bt.to_csv('data/%s-backtest.csv' % id_bt)

## other features data
print('ETL other feature data')
indexes = query('queries/indexes.sql')
indexes.to_csv('data/indexes.csv')

commodities = query('queries/commodities.sql')
commodities.to_csv('data/commodities.csv')

features = load_features(id, cc, load_from, load_to)
features.to_csv('data/%s-feat.csv' % id)

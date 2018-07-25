# -*- coding: utf-8 -*-

import json
from forecaster import forecast
from os import environ
from datetime import datetime
from google.cloud import pubsub

id = environ['TARGET_CFD_ID']
service_id = environ['TARGET_SERVICE_ID']
cc = environ['TARGET_COUNTRY']
# this might be set by default in a GCP env
project_id = environ['GCP_PROJECT']

cfd_opt = {
    'service_id': id,
    'timezone': environ['TIMEZONE'],
    'time_from': environ['TIME_FROM'],
    'time_to': environ['TIME_TO']
}

# TODO: have an editor listen to prediction events instead
def publish_story(direction, probability, id, project_id):
    publisher = pubsub.PublisherClient()

    topic = 'projects/%s/topics/publication-new' % project_id

    emojis = {
        'UP': '☀️',
        'DOWN': '☁️'
    }
    directions_se = {
        'UP': 'upp',
        'DOWN': 'ner'
    }

    template_vars = (
        id,
        directions_se[direction], 
        emojis[direction],
        int(round(probability * 100, 2))
    )

    body = 'Idag gissar roboten att %s kommer gå %s %s\n%s%% självsäker' % template_vars

    payload = {
        'title': '',
        'body': body,
        'created_at': datetime.now().isoformat(),
        'entry_id': 'NA',
        'tags': ['market-forecast-daily']
    }

    data = json.dumps(payload)
    publisher.publish(topic, data.encode())

def publish_prediction(direction, probability, service_id, project_id):
    publisher = pubsub.PublisherClient()

    topic = 'projects/%s/topics/market.prediction' % project_id

    values = {
        'UP': 1,
        'DOWN': 0
    }

    # period string following pandas standard:
    # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    payload = {
        'service_id': service_id,
        'value': values[direction],
        'probability': "{:.2f}".format(probability),
        'period': 'B'
    }
    data = json.dumps(payload)
    publisher.publish(
        topic, data.encode()
    )


(pred_direction, pred_prob) = forecast(id, cc, cfd_opt)

print(
    '[forecaster] prediction: %s, %s, probability: %s' % (id, pred_direction, pred_prob)
)

publish_story(pred_direction, pred_prob, id, project_id)
publish_prediction(pred_direction, pred_prob, service_id, project_id)

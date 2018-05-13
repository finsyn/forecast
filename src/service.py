# -*- coding: utf-8 -*-

import forecaster
import os
import json
from datetime import datetime
from google.cloud import pubsub

# TODO: have an editor listen to prediction events instead
def publish_story(direction, probability):
    publisher = pubsub.PublisherClient()

    topic = 'projects/insikt-e1887/topics/publication-new'

    emojis = {
        'UP': '☀️',
        'DOWN': '☁️'
    }
    directions_se = {
        'UP': 'upp',
        'DOWN': 'ner'
    }

    template_vars = (directions_se[direction], emojis[direction], int(round(probability * 100, 2)))
    body = 'Idag gissar roboten att OMX30 kommer gå %s %s\n%s%% självsäker' % template_vars

    payload = {
        'title': b'' ,
        'body': body,
        'created_at': datetime.now().isoformat(),
        'entry_id': 'NA',
        'tags': ['market-forecast-daily']
    }

    data = json.dumps(payload)
    publisher.publish(topic, data)

def publish_prediction(direction, probability):
    publisher = pubsub.PublisherClient()

    topic = 'projects/insikt-e1887/topics/predictions'

    values = {
        'UP': 1,
        'DOWN': 0
    }

    # period string following pandas standard:
    # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    payload = {
        'service_id': 'market-index_OMX30',
        'value': values[direction],
        'probability': probability,
        'period': 'B'
    }
    data = json.dumps(payload)
    publisher.publish(
        topic, data
    )


(pred_direction, pred_prob) = forecaster.forecast(254, 'indexes.sql')

print(
    '[forecaster] prediction: %s, probability: %s' % (pred_direction, pred_prob)
)

publish_story(pred_direction, pred_prob)
publish_prediction(pred_direction, pred_prob)

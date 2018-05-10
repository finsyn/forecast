# -*- coding: utf-8 -*-

import forecaster
import os
import json
from datetime import datetime
from google.cloud import pubsub

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

def publish_trade(direction, probability):
    publisher = pubsub.PublisherClient()

    topic = 'projects/insikt-e1887/topics/trading'

    payload = {}
    data = json.dumps(payload)
    publisher.publish(
        topic, data,
        action='open',
        direction=direction,
        service_id='market-index_OMX30'
    )


(pred_direction, pred_prob) = forecaster.forecast(254, 'indexes.sql')

print(
    '[forecaster] prediction: %s, probability: %s' % (pred_direction, pred_prob)
)

result = {
    'direction': pred_direction,
    'probability': str(pred_prob)
}

publish_story(pred_direction, pred_prob)
publish_trade(pred_direction, pred_prob)

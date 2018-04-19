# -*- coding: utf-8 -*-

import forecaster
import os
import json
import logging
from datetime import datetime
from google.cloud import pubsub

def publish(direction, probability):
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


(pred_direction, pred_prob) = forecaster.forecast(254, 'indexes.sql')

logging.info(
    '[forecaster] prediction: %s, probability: %s' % (pred_direction, pred_prob)
)

result = {
    'direction': pred_direction,
    'probability': str(pred_prob)
}

publish(pred_direction, pred_prob)

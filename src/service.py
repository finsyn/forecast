# -*- coding: utf-8 -*-

import json
import time
from forecaster import forecast
from os import environ
from datetime import datetime
from google.cloud import pubsub_v1

# Read more over at
# https://cloud.google.com/pubsub/docs/publisher#pubsub-publish-message-python

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

def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
       print('[forecaster] Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print('[forecaster] Published message: {}'.format(
            message_future.result()
        ))

def publish_message(data, topic_name, project_id):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    message_future = publisher.publish(
        topic_path, data=data.encode('utf-8')
    )
    message_future.add_done_callback(callback)


# TODO: have an editor listen to prediction events instead
def publish_story(direction, probability, id, project_id):

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
    publish_message(data, 'publication-new', project_id)


def publish_prediction(direction, probability, service_id, project_id):

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
    publish_message(data, 'market-prediction', project_id)
    
(pred_direction, pred_prob) = forecast(id, cc, cfd_opt)

print(
    '[forecaster] prediction: %s, %s, probability: %s' % (id, pred_direction, pred_prob)
)

publish_story(pred_direction, pred_prob, id, project_id)
publish_prediction(pred_direction, pred_prob, service_id, project_id)

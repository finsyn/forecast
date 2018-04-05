# -*- coding: utf-8 -*-

import SimpleHTTPServer
import SocketServer
import forecaster
import os
import json
import logging
from datetime import datetime
from google.cloud import pubsub


PORT = 8080
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

class ForecasterHandler(Handler):

    def publish(self, direction, probability):
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


    def do_GET(self):
        if 'X-Appengine-Cron' in self.headers:
            (pred_direction, pred_prob) = forecaster.forecast(254, 'indexes.sql')
            logging.info(
                '[forecaster] prediction: %s, probability: %s' % (pred_direction, pred_prob)
            )
            result = {
                'direction': pred_direction,
                'probability': str(pred_prob)
            }
            self.publish(pred_direction, pred_prob)
            self.send_response(200)
        else:
            result = {
                    'msg': 'method not allowed'
                    }
            self.send_response(405)

        body = bytes(json.dumps(result))
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

httpd = SocketServer.TCPServer(("", PORT), ForecasterHandler)
logging.info('[forecaster] serving at port: %s' % PORT)
httpd.serve_forever()

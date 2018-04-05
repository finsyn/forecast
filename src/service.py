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

    def publish(self, result):
        publisher = pubsub.PublisherClient()

        topic = 'projects/insikt-e1887/topics/publication-new'

        body = 'FinSyn tror att OMX30 kommer gå %s idag med %s sannolikhet' % (result['direction'], result['probability'])

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
            self.publish(result)
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

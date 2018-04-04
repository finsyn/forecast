import SimpleHTTPServer
import SocketServer
import forecaster
import os
import json
import logging

PORT = 8080
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

class ForecasterHandler(Handler):

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

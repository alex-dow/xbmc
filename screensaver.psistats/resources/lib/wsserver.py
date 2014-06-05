import pika
import sys, time
import socket
import threading
import json
from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
import argparse

parser = argparse.ArgumentParser(description='Psistats Screensaver for XBMC - Websockets Host')
parser.add_argument('--listen-ip', default='0.0.0.0', help='IP Address to listen to', dest='listen-ip')
parser.add_argument('--listen-port', default='9999', help='Port to listen to', dest='listen-port')
parser.add_argument('--psistats-ip', default='127.0.0.1', help='Psistats RabbitMQ Server', dest='psistats-ip')
parser.add_argument('--psistats-port', default='5672', help='Psistats RabbitMQ Port', dest='psistats-port')
parser.add_argument('--psistats-prefix', default='psistats', help='Psistats Prefix', dest='psistats-prefix')
parser.add_argument('--psistats-exchange', default='psistats', help='Psistats exchange name', dest='psistats-exchange')
parser.add_argument('--queue', default='psistats-aggregate', help='Aggregate queue name', dest='queue')

options = vars(parser.parse_args())

connection = pika.BlockingConnection(pika.ConnectionParameters(
    options['psistats-ip'], int(options['psistats-port'])
))

channel = connection.channel()

channel.queue_declare(queue=options['queue'], durable=False, auto_delete=True, arguments={'x-message-ttl': 30000})
channel.queue_bind(queue=options['queue'], exchange=options['psistats-exchange'], routing_key=options['psistats-prefix'] + '.*')

def callback(ch, method, properties, body):
    print body

class DoWork(threading.Thread):

    def __init__(self, ws):
        super(DoWork, self).__init__()
        self.ws = ws
        self.RUNNING = True
        self.msg_counter = 0

    def run(self):
        while self.RUNNING:
            if self.ws.client_terminated == True or self.ws.server_terminated == True:
                print "WebSocket Terminated"
                self.RUNNING = False
            self.msg_counter = 0
            try:
                while self.msg_counter < 20:
                    mframe, hframe, body = channel.basic_get(options['queue'], no_ack=True)
                    if mframe:
                        
                        try:
                            body = body.strip()
                            body = body.replace('\x00','') # fixes some strange problem with windows machines
                            j = json.loads(body)
                        except ValueError:
                            print "Failed loading json string:"
                            print repr(body)
                            continue
                        
                        try:
                            j_str = json.dumps(j)
                        except ValueError:
                            print "Failed creating json object:"
                            print j
                            continue
                        print j_str
                        self.ws.send(j_str, False)
                        time.sleep(0.01)
                        self.msg_counter = self.msg_counter  + 1
                    else:
                        break
                time.sleep(0.5)
            except:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
                self.RUNNING = False
        
        

class WebSocketHandler(WebSocket):

    RUNNING = True

    def received_message(self, message):
        print "received message"
        print message
        thread = DoWork(self)
        thread.start()


server = make_server(options['listen-ip'], int(options['listen-port']), 
    server_class=WSGIServer, 
    handler_class=WebSocketWSGIRequestHandler,
    app=WebSocketWSGIApplication(handler_cls=WebSocketHandler))

server.initialize_websockets_manager()
print "starting server"
server.serve_forever()
channel.close()


"""
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.1.101', 25672
))

channel = connection.channel()

channel.queue_declare(queue='psistats-aggregate', durable=False, arguments={'x-message-ttl': 5000})
channel.queue_bind(queue='psistats-aggregate', exchange='psistats', routing_key='psistats.*')

def callback(ch, method, properties, body):
    print body



channel.basic_consume(callback, queue="psistats-aggregate")

channel.start_consuming()
"""

import pika
import sys, time
import socket
import server.handshake
import threading
import json
from wsgiref.simple_server import make_server
from ws4py.websocket import WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication
connection = pika.BlockingConnection(pika.ConnectionParameters(
    '192.168.1.101', 25672
))

channel = connection.channel()

channel.queue_declare(queue='psistats-aggregate', durable=False, auto_delete=True, arguments={'x-message-ttl': 5000})
channel.queue_bind(queue='psistats-aggregate', exchange='psistats', routing_key='psistats.*')

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
                    mframe, hframe, body = channel.basic_get('psistats-aggregate', no_ack=True)
                    if mframe:
                        
                        try:
                            body = body.strip()
                            body = body.replace('\x00','')
                            j = json.loads(body)
                        except ValueError:
                            print "Bad JSON:"
                            print repr(body)
                            continue
                        
                        try:
                            j_str = json.dumps(j)
                        except ValueError:
                            print "Failed dumping json:"
                            print j
                            continue
                        print j_str
                        self.ws.send(j_str, False)
                        time.sleep(0.1)
                        self.msg_counter = self.msg_counter  + 1
                    else:
                        break
                time.sleep(0.5)
            except:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
                self.RUNNING = False
        
        

class EchoWebSocket(WebSocket):

    RUNNING = True

    def received_message(self, message):
        print "received message"
        thread = DoWork(self)
        thread.start()


server = make_server('', 9999, 
    server_class=WSGIServer, 
    handler_class=WebSocketWSGIRequestHandler,
    app=WebSocketWSGIApplication(handler_cls=EchoWebSocket))

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

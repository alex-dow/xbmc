import socket
import argparse
import os
from thread import *

CONTENT_TYPE_MAP = {
    "html": "text/html",
    "js": "text/javascript",
    "css": "text/css",
    "png": "image/png",
    "jpg": "image/jpg",
    "gif": "image/gif"
}

parser = argparse.ArgumentParser(description='XBMC Psistats Screensaver - HTTP Server')
parser.add_argument('--listen-ip', default='127.0.0.1', help='IP Address to listen to', dest='listen-ip')
parser.add_argument('--listen-port', default='10102', help='Port to bind to', dest='listen-port')
parser.add_argument('--root-dir', default='../web', help='Root folder containing the index.html file', dest='root-dir')

options = vars(parser.parse_args())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((options['listen-ip'], int(options['listen-port'])))
s.listen(5)

def handle_connection(conn):
    print "Handling connection"
    http_headers = False
    data = ""
    try:
        while http_headers == False:
        
            data = data + conn.recv(128)
            if "\r\n\r\n" in data:
                http_headers = True
                headers = data.split("\r\n\r\n", 1)[0].split("\r\n")
                requested_file = options['root-dir'] + headers[0].split(" ")[1]

                filetype = requested_file.split('.')[-1]
                print "Requested file: %s" % requested_file
                print "Requested filetype: %s" % filetype

                response_headers = [
                    "HTTP/1.x 200 OK",
                    "Connection: close",
                    "Content-type: %s" % CONTENT_TYPE_MAP[filetype],
                    "Content-length: %s" % os.path.getsize(requested_file)
                ]

                for idx in response_headers:
                    conn.send(idx + "\r\n")
                conn.send("\r\n")
                
                with open(requested_file, "rb") as f:
                    while True:
                        b = f.read(128)
                        if b:
                            conn.send(b)
                        else:
                            break

                

    finally:                
        conn.close()

RUNNING = True

try:
    while RUNNING:
        c, addr = s.accept()
        print "Connection from ", addr
        start_new_thread(handle_connection, (c, ))
finally:
    s.close()

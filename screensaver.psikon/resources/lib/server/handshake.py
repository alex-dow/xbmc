import base64
import hashlib

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class InvalidHandshake(Exception):
    pass

def split_headers(header_string):
    headers = {}
    for header in header_string.split('\r\n'):
        header_parts = header.split(':',1)
        print header_parts
        headers[header_parts[0]] = header_parts[1].strip()
    return headers

def check_headers(headers):
    try:
        assert headers['Upgrade'].lower() == 'websocket'
        assert len(base64.b64decode(headers['Sec-WebSocket-Key'].encode())) == 16
    except AssertionError as exc:
        raise InvalidHandshake("Header had wrong value")
    except KeyError as exc:
        raise InvalidHandshake("Missing headers")

def accept(key):
    sha1 = hashlib.sha1((key + GUID).encode()).digest()
    return base64.b64encode(sha1).decode()

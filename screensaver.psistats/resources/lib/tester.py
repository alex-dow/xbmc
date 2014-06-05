import server.handshake

headers = 'Foo: bar\r\nHello: world\r\n\r\n'

print server.handshake.split_headers(headers.split('\r\n\r\n', 1)[0])


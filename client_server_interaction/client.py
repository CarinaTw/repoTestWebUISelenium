import socket

HOST = socket.gethostname()
PORT = 8889

with socket.socket() as s:
    s.connect((HOST, PORT))
    received_data = s.recv(1024)

    data_to_send = "HTTP/1.1 200 OK\n Content-Length: 100\n Connection: close\n Content-Type: text/html\n\n HELLO".encode("utf-8")

    s.send(data_to_send)
    data = s.recv(1024)
    print('Received', repr(data))

import socket
import re

HOST = socket.gethostname()
PORT = 8889

with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        conn.send("Whats up man, Im Server!".encode("utf-8"))
        while True:
            data = conn.recv(1024)

            if not data:
                print("No data has received. Connection closed")
                break
            data = data.decode("utf-8")
            print(data)

            data_to_send = re.split("\n", data)
            print(data_to_send)

            lst = []
            for i in data_to_send:
                if re.findall(":", i):
                    kv = i.split(":")
                    lst.append(kv[0])
                else:
                    lst.append(i)

            print(lst)
            for i in lst:
                conn.send(i.encode("utf-8"))


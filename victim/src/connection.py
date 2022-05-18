import os
import socket
import sys

IP = "172.20.10.2"
PORT = 4444

# Selects family IPv4 to connect to with TCP 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect(ip: str, port: int):
    server_address = (ip, port)
    while True:
        try:            
            # Connect to host (add timeout?)
            sock.connect((ip, port))
            
            break
        except:
            continue
    
    sock.send(str.encode("Succesfully connected\n"))
    
    return sock
